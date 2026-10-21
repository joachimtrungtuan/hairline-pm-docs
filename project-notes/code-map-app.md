# Code Map — hairline-app (Flutter / Dart, clean architecture; the Patient mobile client — iOS/Android)

Curated folder-group map (folder-level, not file-level — refresh when modules are
added/restructured, flagged by check-code-map-drift.sh). For the SIGNATURES of one
subdir on demand (do NOT persist): repomix <subdir> --compress --remove-comments --style markdown -o -
**Locator, not evidence:** this map tells you WHERE to look; read the actual source for any
finding. It exists to prevent broad searches, never to replace reading the code.
**Built from:** `main/hairline-app` @ `5516c18` (HEAD commit dated 2026-08-05); map refreshed 2026-10-21.
Compare with `git -C main/hairline-app rev-parse --short HEAD` — if HEAD has moved, the code wins.

This is the Patient platform only (P-0x modules); Provider/Admin live in the web
frontend. Built in Flutter with clean architecture: each feature under
`lib/src/features/<feature>/` splits into `data/` (datasources, models, repository
impls), `domain/` (entities, repository interfaces, usecases), and `presentation/`
(providers = state, ui = screens). State management uses Provider/ChangeNotifier
(`*_provider.dart`). Dependency wiring is in `di/`. The app consumes the shared
Laravel API. Note: the tech-spec's "React Native (recommended)" mobile section is
stale — the actual implementation is Flutter.

## di/
- **Purpose:** Dependency injection container (get_it style): registers datasources, repositories, usecases, providers; `multi_providers.dart` wires the widget-tree Providers.
- **Modules:** — (infra).
- **FRs:** —.
- **Entry points / key files:** `di/injection_container.dart`, `di/multi_providers.dart`.

## src/core/
- **Purpose:** Cross-cutting foundation. `data/` = API client (`api.dart`, `api_response.dart`), secure storage, draft storage; `domain/` = base `UseCase`, `Failure`; `navigation/` = navigation service; `widgets/` = shared UI primitives (buttons, text fields, dropdowns, calendar, country dropdown, rating slider, network image).
- **Modules:** — (cross-cutting infra), S-05.
- **FRs:** —.
- **Entry points / key files:** `core/data/api.dart`, `core/navigation/navigation_service.dart`, `core/widgets/core_widgets_export.dart`.

## src/features/authentication/
- **Purpose:** Patient auth & onboarding: login, signup (multi-step: name → email/password → OTP → create profile → discover; `signup/widgets/`), forgot/reset password, change password (`presentation/change_password/`), OTP verify, resend activation, complete profile, patient discovery questions.
- **Modules:** P-01.
- **FRs:** FR-001.
- **Entry points / key files:** `presentation/login/ui/login_screen.dart`, `presentation/signup/ui/`, `domain/usecases/login_usecase.dart`.

## src/features/request/
- **Purpose:** Inquiry/quote-request creation flow: hair-concerns, transplant area selection, destination/country selection, popular provider selection, multi-step request (questions, head scan, schedule, summary, complete), draft inquiry handling.
- **Modules:** P-02, P-07.
- **FRs:** FR-002, FR-003.
- **Entry points / key files:** `presentation/request_steps/request_progress_steps.dart`, `presentation/transplant_request/transplant_request_begin.dart`, `domain/usecases/create_inquiry_usecase.dart`.

## src/features/dashboard/
- **Purpose:** The patient home hub and largest feature — the full post-inquiry journey. Sub-screens: offers/offers-overview & offer-accept (quote comparison incl. `offers/compare_offer_ui/` + acceptance + discount code), cancel_inquiry, provider_screen (provider detail, quote request, related questions, video player), requested/request-overview (medical history view, 3D scan view), request_confirmed, scheduled (appointment detail), travel_logistics + `inprogress/travel_itinerary/` (flight/hotel details & itinerary), inprogress (booking/problem/provider/treatment tabs), offer_accepted, review_form, aftercare (milestone: pain level/question/scan-head, medication/milestone/overview tabs), `purchse_aftercase/` (sic — standalone aftercare purchase wizard: services → external treatment details → checkout). Also `presentation/policy/` (cancellation/privacy/terms screens), `presentation/home/notifications/` (notification list, filter, search), and `services/` (FCM device-token registration). Models/entities cover quotes, inquiries, offers, treatments, payment intents, questionnaires, milestones.
- **Modules:** P-02, P-03, P-04, P-05, S-03.
- **FRs:** FR-003, FR-005, FR-006, FR-007, FR-007B, FR-008, FR-011, FR-013, FR-020, FR-027.
- **Entry points / key files:** `presentation/dashboard/dashboard_tab.dart`, `presentation/dashboard/offers/offers_overview_screen.dart`, `presentation/dashboard/aftercare/after_care_tabs.dart`, `domain/usecases/accept_quote_usecase.dart`.

## src/features/head_scan/
- **Purpose:** Full clean-architecture head-scan feature (data/domain/presentation): guided capture with on-device head-orientation detection (`controllers/`, `workers/`, bundled model assets under `presentation/python/`), tutorial/guide, analyzing/complete screens, scan history by day and month, per-day detail, and annotation pins (add/edit points). Upload via `upload_head_scan_images_usecase`.
- **Modules:** P-07, P-05.
- **FRs:** FR-002, FR-037 (see Notes).
- **Entry points / key files:** `presentation/screens/head_scan_capture_screen.dart`, `presentation/providers/head_scan_provider.dart`, `data/datasources/head_scan_api.dart`.

## src/features/library/
- **Purpose:** Library tab listing past scan records by year (`library_tab.dart`); currently populated from a hard-coded in-widget record list, not an API.
- **Modules:** P-07.
- **FRs:** — (see Notes).
- **Entry points / key files:** `presentation/library_tab.dart`.

## src/features/messages/
- **Purpose:** Conversation list + 1:1 chat (patient↔provider) with message timeline.
- **Modules:** P-06.
- **FRs:** FR-012.
- **Entry points / key files:** `presentation/one_to_one_chat_screen/ui/one_to_one_chat_screen.dart`, `presentation/message_tab.dart`.

## src/features/calls/
- **Purpose:** Voice/video calling via Twilio: token generation, initiate/join/end call, call history, incoming-call sheet, call notification service, permission helper.
- **Modules:** P-06, S-03.
- **FRs:** FR-012.
- **Entry points / key files:** `presentation/ui/call_screen.dart`, `services/twilio_call_service.dart`, `domain/usecases/initiate_call_usecase.dart`.

## src/features/profile/
- **Purpose:** Patient profile & support: edit profile, settings (+ `setting/provider/` state), important information, my_treatments (treatment history cards), payment_methods (saved methods list/detail), reviews (view + submit patient→provider reviews), help & support (support chat, contact support), logout.
- **Modules:** P-01, P-03, P-06, P-08.
- **FRs:** FR-001, FR-007, FR-013, FR-035.
- **Entry points / key files:** `presentation/edit_profile/ui/edit_profile_screen.dart`, `presentation/help_support/ui/help_support_screen.dart`, `presentation/review/ui/review_screen.dart`.

## src/features/location/
- **Purpose:** Location/country lookup data feeding request & profile flows.
- **Modules:** P-02 (supports), S-04.
- **FRs:** FR-008, FR-022.
- **Entry points / key files:** `domain/usecases/get_locations_usecase.dart`, `data/datasources/location_api.dart`.

## src/features/common/
- **Purpose:** Shared error-message model/entity reused across features.
- **Modules:** — (cross-cutting).
- **FRs:** —.
- **Entry points / key files:** `data/models/error_message_model.dart`.

## src/features/splash/ + features/home/
- **Purpose:** App entry: splash, landing screen; `dashboard/presentation/home` hosts the bottom-nav home shell + notification tab.
- **Modules:** P-01, S-03.
- **FRs:** FR-001, FR-020.
- **Entry points / key files:** `splash/splash_screen.dart`, `splash/landing_screen.dart`, `features/dashboard/presentation/home/home_screen.dart`.

## services/ (top-level lib/services)
- **Purpose:** Cross-feature services: image picker (camera/gallery) used by head-scan capture and profile.
- **Modules:** P-07, S-05.
- **FRs:** FR-002.
- **Entry points / key files:** `services/image_picker/image_picker_services.dart`.

## utils/
- **Purpose:** App-wide constants & helpers: assets, colors, sizes, strings, toasts, loader, global functions, utilities.
- **Modules:** — (cross-cutting).
- **FRs:** —.
- **Entry points / key files:** `utils/utils_export.dart`, `utils/strings.dart`, `utils/colors.dart`.

## lib root (main.dart, hair_line_export.dart)
- **Purpose:** App bootstrap (`main.dart` — runApp, DI init, root MaterialApp) and the barrel export aggregating feature exports.
- **Modules:** — (infra).
- **FRs:** —.
- **Entry points / key files:** `main.dart`, `hair_line_export.dart`.

## dummy/ (lib/dummy)
- **Purpose:** Static prototype screens (dashboard, offers, request, travel, in-progress, treatment) reachable from `splash/landing_screen.dart`; demo/UI mock-ups, not the live flow.
- **Modules:** — (prototype).
- **FRs:** —.
- **Entry points / key files:** `dummy/dummy_dashboard_screen.dart`.

## Notes / unmapped
- "3D scan" (P-07 / FR-002) is V1 = a guided head-photo set, not true 3D — see request `request_step_headscan.dart` and `requested/scan_3d_view_screen.dart` (image gallery viewer).
- Aftercare lives INSIDE `features/dashboard/presentation/dashboard/aftercare/` rather than its own top-level feature — patient aftercare (P-05/FR-011) is reached through the dashboard journey, not a separate module folder.
- `features/profile` carries both profile editing AND support/help + reviews; reviews (FR-013) and support (FR-035) are not separate feature folders.
- The tech-spec Mobile Architecture section describes React Native and is stale; this Flutter structure is authoritative.
- `features/head_scan` day/month summaries and annotations point to progress monitoring (FR-037 hair-loss monitoring); whether it also serves FR-038 transplant-progress monitoring is not confirmed from the code — check the API usage before relying on that split.
- `features/library` uses hard-coded records, so no FR binding is asserted until it reads live data.
- `lib/dummy/` and `purchse_aftercase` (misspelled folder name in source) — search with the source spelling.
- FR bindings are best-effort from PRD module codes; `—` = cross-cutting/infra.
