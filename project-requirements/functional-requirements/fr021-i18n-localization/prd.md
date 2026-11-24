# FR-021 - Multi-Language & Localization

**Module**: P-01: Patient Account & Settings | PR-06: Profile & Settings Management | A-09: System Settings & Configuration | S-02: Payment Processing Service | S-03: Notification Service
**Feature Branch**: `fr021-i18n-localization`
**Created**: 2025-11-11
**Status**: ✅ Verified & Approved
**Source**: FR-021 from `local-docs/project-requirements/system-prd.md`; client transcriptions; product-defined localization operations

---

## Executive Summary

FR-021 defines Hairline's multi-language and localization capability across the Patient App, Provider Dashboard, Admin Platform, and system-delivered communications. The feature lets users choose a preferred interface language, lets the system serve translated UI and notification text with fallback behavior, and gives Admin a controlled way to manage supported locales, translation keys, translation values, JSON import/export, published translation versions, rollback, and coverage reporting.

The client requirement establishes multilingual behavior and editable language content, but the transcriptions do not define a detailed technical operating model for translation management. This PRD therefore specifies a product-owned hybrid approach:

1. A canonical translation registry stores every translatable key, English source value, metadata, lifecycle state, and locale values.
2. Admin users edit translation rows and key details for precise copy updates.
3. Admin users import/export JSON files for translator handoff and bulk translation work.
4. Inline edits and imports create draft changes only.
5. Published translation bundles are the only translation packages served to Patient, Provider, and Admin runtime clients.
6. Every publish creates an immutable version; rollback creates a new version restoring a prior published bundle.
7. Machine translation is an admin-controlled draft-generation accelerator for a whole target language/locale; it never publishes directly and never replaces the English source locale.

Initial supported languages are English (`en`) and Turkish (`tr`). Additional languages are expandable. RTL languages such as Arabic are planned, with V1 requiring locale metadata and implementation readiness, but not full RTL layout delivery. (REQ-021-057)

---

## Module Scope

### Multi-Tenant Architecture

- **Patient Platform (P-01)**: Patient selects app language from Settings; Patient App fetches published patient-app translation bundles and applies fallback when translations are missing.
- **Provider Platform (PR-06)**: Provider users switch dashboard interface language from the top bar; Provider Dashboard fetches published provider-dashboard translation bundles. Provider profile spoken languages remain separate profile data.
- **Admin Platform (A-09)**: Admin users switch dashboard interface language from the top bar and manage localization through dedicated screens for locales, translation registry, key detail editing, JSON import/export, publish/version history, rollback, and coverage.
- **Shared Services (S-02 / S-03)**: S-02 supports localized currency display and conversion rules. S-03 consumes FR-021 supported locales and fallback rules for notification template selection and delivery.

### Multi-Tenant Breakdown

**Patient Platform (P-01)**:

- Patient can select an active supported language from Patient App Settings.
- Patient language preference persists across sessions/devices where account sync exists.
- Patient App loads the latest published patient-app translation bundle for the selected locale.
- Patient App displays fallback text when a selected-locale value is missing.
- Patient App continues to show user-generated content in the language originally entered by the user; when free-text translation is on, free text written by others is shown translated into the patient's own language (General Module Rule 15). (REQ-021-064)

**Provider Platform (PR-06)**:

- Provider users can select dashboard UI language from the Provider Dashboard top bar.
- Provider Dashboard loads the latest published provider-dashboard translation bundle for the selected locale.
- Provider UI language preference does not overwrite provider profile spoken-language selections.
- Provider profile language chips consume the central language/locale catalog where appropriate, but represent languages spoken by the clinic/provider rather than UI translation preference.

**Admin Platform (A-09)**:

- Admin users can select Admin Platform UI language from the top bar.
- Admin can manage supported locales, default locale, locale activation state, native names, text direction metadata, and fallback order.
- Admin can view and edit translation keys/values through registry and key-detail screens.
- Admin can import/export translation JSON files by locale, tenant/surface, group, and version.
- Admin can manage machine-translation provider API credentials and run controlled machine-translation jobs for a selected non-English language.
- Admin can switch free-text translation on or off for the platform and set its monthly budget.
- Admin can publish draft changes into versioned bundles and roll back to prior published versions.
- Admin can inspect coverage, missing keys, review-needed keys, and version history.

**Shared Services (S-02 / S-03)**:

- Shared localization service provides published bundles, version metadata, cache invalidation metadata, and fallback resolution.
- S-03 Notification Service selects notification language using recipient preference and FR-021 fallback rules while FR-030 owns template authoring.
- S-02 Payment Processing Service provides currency conversion source and formatting rules where localized currency display is required.
- Shared audit/logging captures localization changes, publish actions, rollback actions, and missing-translation events.

### Communication Structure

**In Scope**:

- Localized UI labels, navigation labels, validation messages, status labels, empty states, system guidance, and system-controlled static text.
- Localized notification template selection and fallback behavior for email/push where notification content is supplied by FR-030.
- Missing-translation logging and admin-facing coverage reporting.
- Admin publish/rollback audit records and import history.
- Admin-managed machine-translation provider configuration and draft generation for non-English target languages.
- Machine translation of free text written by one user for another, shown to the reader when the Admin switch is on (General Module Rules 15 and 16).

**Out of Scope**:

- Machine translation of uploaded documents, and of any user-generated content other than the free text listed in General Module Rule 15. (REQ-021-056)
- Full notification-template authoring, variable management, and channel-specific template preview; these remain in FR-030 (see REQ-030-006 and REQ-030-152).
- Legal document versioning and acceptance tracking; these remain in FR-027 (see REQ-027-036, REQ-027-002, and REQ-027-029).
- Machine translation of system-controlled text as an automatic runtime translator or direct-to-production publishing path; the reader-facing translation of free text is the separate case in General Module Rule 15.
- Full RTL layout delivery in V1.

### Entry Points

- Patient opens Patient App > Settings > Language & Region.
- Provider user opens the Provider Dashboard top-bar language selector.
- Admin user opens the Admin Platform top-bar language selector.
- Admin opens Admin Platform > Settings > Localization.
- Admin exports English/source JSON for translator handoff.
- Admin imports translated JSON for a target locale.
- Admin configures a machine-translation provider API key from Admin Platform > Settings > Localization > Machine Translation.
- Admin generates machine-translated draft values for a selected non-English language.
- Admin publishes pending localization changes from Language Version History & Rollback.
- Admin rolls back a published translation bundle from Language Version History & Rollback.
- Runtime clients fetch published translation bundles on app start, language change, cache revalidation, or version change. (REQ-021-113)

---

## Business Workflows

### Main Flow: Admin Updates and Publishes Translation Version

**Actors**: Admin (an admin holding the Manage Localization permission, REQ-021-122), Super Admin (English source edits, default locale change, publish, and rollback), System
**Trigger**: Admin needs to update translations through either individual text patching or JSON package import, then make those changes live
**Outcome**: System validates the selected update mode, saves individual patches as draft, either imports JSON packages as draft or publishes them as a version, and makes published bundles available to runtime clients

**Flow Diagram**:

```mermaid
flowchart TD
  S1["1. Admin opens Localization Management"] --> S2{"2. What action is needed?"}
  S2 -->|Update translations| S3{"3. Which update mode is needed?"}
  S2 -->|Rollback published version| R1["3R. Admin selects prior published version from Version History"]
  R1 --> R2["4R. System displays impacted locale, tenant/surface, groups, keys, and rollback warning"]
  R2 --> R3["5R. Admin enters rollback reason and confirms"]
  R3 --> R4["6R. System creates new rollback version using prior bundle contents and marks it active"]
  R4 --> S15
  S3 -->|Individual text patching| P1["4P. Admin selects a key from Translation Key Inventory and edits values in Translation Key Detail Editor"]
  S3 -->|JSON package import| J1["4J. Admin uploads JSON package for selected locale, tenant/surface, and group (an import into the English source locale is an English source edit, REQ-021-123)"]
  S3 -->|Machine translation| M1["4M. Admin follows Alternative Flow C1 (Machine Translation Draft Generation)"]
  P1 --> P2{"5P. English source value changed?"}
  P2 -->|Yes| P3["6P. System requires Super Admin authorization, change reason, and the optional non-semantic confirmation"]
  P3 --> P5
  P2 -->|No| P5["7P. System validates placeholders, ICU syntax, required values, and length guidance"]
  P5 --> P6{"8P. Patch valid?"}
  P6 -->|No| E1["9. System blocks save/import/publish and shows errors for correction"]
  P6 -->|Yes| P4["9P. After validation passes, if the English value changed, system marks dependent non-English translations Review Needed unless the edit is confirmed non-semantic"]
  P4 --> D1["9A. System saves accepted changes as draft and marks keys Pending Publish"]
  M1 --> D1
  J1 --> J2["5J. System validates JSON syntax, known keys, duplicate keys, placeholders, ICU syntax, locale compatibility, and unsupported/orphaned keys"]
  J2 --> J3{"6J. Structural error found?"}
  J3 -->|Yes| E1
  J3 -->|No| J4["7J. System shows validation preview with created, updated, unchanged, skipped, row-warning, and error counts"]
  J4 --> J5{"8J. Row-level errors or warnings?"}
  J5 -->|Yes| J6["9J. Admin chooses whether to import valid rows only as a draft (publish is a separate later action) or cancel for correction"]
  J6 -->|Cancel| E1
  J6 -->|Import valid rows only, as a draft| D1
  J5 -->|No| J7{"10J. Import decision after validation preview?"}
  J7 -->|Import as Draft| D1
  J7 -->|Import and Publish Version| IP1["11J. Admin enters publish summary and confirms import + publish"]
  D1 --> V1["10. Admin opens Language Version History & Rollback and reviews pending changes, coverage, warnings, and previous active version"]
  V1 --> V2["11. Admin enters publish summary and confirms publish"]
  IP1 --> V3
  V2 --> V3{"12. Publish validation passed?"}
  V3 -->|No| E1
  V3 -->|Yes| V4["13. System creates immutable published bundle version and marks it active"]
  V4 --> S15["14. System invalidates cache/version metadata for impacted bundles"]
  S15 --> S16["15. Runtime clients receive new text on next fetch, refresh, or cache revalidation"]
```

### Alternative Flows

**A1: User Selects Language**

- **Trigger**: Patient, Provider, or Admin changes interface language.
- **Outcome**: User interface loads selected locale from latest published bundle, with fallback for missing keys.
- **Flow Diagram**:

```mermaid
flowchart TD
  A1S1["1. User opens tenant-specific language selector"] --> A1S2["2. System displays active supported locales only"]
  A1S2 --> A1S3["3. User selects locale"]
  A1S3 --> A1S4["4. System persists language preference"]
  A1S4 --> A1S5["5. System fetches latest published bundle for selected locale and tenant/surface"]
  A1S5 --> A1S6["6. UI reloads or re-renders localized text"]
```

**B1: Missing Translation**

- **Trigger**: Runtime client requests a key that has no value in the selected locale.
- **Outcome**: System displays fallback text and logs the missing key for coverage reporting.
- **Flow Diagram**:

```mermaid
flowchart TD
  B1S1["1. Client requests translated value for selected locale"] --> B1S2{"2. Locale value exists in active published bundle?"}
  B1S2 -->|Yes| B1S3["3. System displays selected-locale value"]
  B1S2 -->|No| B1S4["4. System checks configured fallback order"]
  B1S4 --> B1S5["5. System displays fallback value"]
  B1S5 --> B1S6["6. System logs missing key with locale, tenant/surface, and fallback used"]
```

**C1: Machine Translation Draft Generation**

- **Trigger**: Admin wants to quickly prepare a non-English target language using configured machine translation.
- **Outcome**: System creates machine-generated draft values for the selected language; Admin must review and publish through the standard version workflow before runtime clients receive the text.
- **Flow Diagram**:

```mermaid
flowchart TD
  C1S1["1. Admin opens Machine Translation Provider & Draft Generation"]
  C1S1 --> C1S2{"2. Enabled provider with a Connected status?"}
  C1S2 -->|No| C1S3["3. Admin adds provider, API key, supported languages, and usage notes, or enables an existing provider"]
  C1S3 --> C1S4["4. System stores encrypted credential and verifies connection"]
  C1S4 --> C1S4A{"4A. Connection verified?"}
  C1S4A -->|No| C1S4B["4B. System sets the provider status to Error and stops; no job starts"]
  C1S4A -->|Yes| C1S5
  C1S2 -->|Yes| C1S5["3. Admin selects target language, tenant/surface scope, and generation mode"]
  C1S5 --> C1S6{"5. Generation mode?"}
  C1S6 -->|Prefill missing keys| C1S7["6A. System previews the keys it would translate"]
  C1S6 -->|Replace entire language| C1S8["6B. System previews the keys it would replace"]
  C1S7 --> C1S7A["6C. Admin reviews the preview counts, enters a reason, and confirms"]
  C1S8 --> C1S7A
  C1S7A --> C1S7B["6D. System runs the job and validates placeholders, ICU syntax, protected terms, unsupported keys, and provider response errors"]
  C1S7B --> C1S9["7. System saves the values that pass validation as drafts marked Review Needed, records failed rows in job history, and sets the job status"]
  C1S9 --> C1S10["8. Admin reviews draft values in registry/key detail and publishes through Screen 9 when ready"]
```

---

## Screen Specifications

### Patient Platform

#### Screen 1: Patient App - Language & Region Settings

**Purpose**: Allow patients to choose the language used by the Patient App and review region-dependent display settings.

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules | Graph field |
| --- | --- | --- | --- | --- | --- |
| Language | select | Yes | Patient's preferred app language | Must be an active supported locale | ENT-patient.preferred_language, ENT-locale.english_name, ENT-locale.native_name |
| Region/Locale | select | No | Regional formatting context for dates, numbers, and currency display | Must be a supported locale/region option when exposed (REQ-021-063) | ENT-patient.preferred_region |
| Timezone | select | No | Patient's preferred timezone for appointment and treatment schedule display | Must be a value from the FR-026 GMT list; fixed offsets do not follow daylight saving (REQ-021-062) | ENT-patient.preferred_timezone |
| Fallback notice | read-only text | No | Explains that some text may appear in the default language when translation is missing | Display only when fallback has occurred (REQ-021-118) | no graph field (display notice) |

**Business Rules**:

- Language selection is stored on the patient profile/account preference. (REQ-021-058)
- Bundle loading for the Patient App follows General Module Rule 14.
- See REQ-021-013.
- See REQ-021-017 and REQ-021-037.
- If a locale is deactivated, patients who previously selected it are moved to fallback behavior without deleting their historical preference. (REQ-021-060)
- See REQ-021-076.
- See REQ-021-118.
- When timezone preference is null or unset, the Patient App uses the device/browser-detected timezone; if unavailable, it falls back to UTC and displays a visible timezone indicator so the patient knows which timezone is in use. (REQ-021-061)

**Notes**:

- The language control lives inside the Settings menu, not in primary navigation.
- The selected language applies to navigation labels, button labels, validation messages, empty states, system-controlled status labels, and static UI guidance. (REQ-021-005)
- See REQ-021-064.

---

### Provider Platform

#### Screen 2: Provider Dashboard - Top-Bar Language Selector

**Purpose**: Allow provider users to switch the Provider Dashboard interface language without leaving their current workflow.

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules | Graph field |
| --- | --- | --- | --- | --- | --- |
| Current language | dropdown | Yes | Currently selected dashboard language | Must be an active supported locale | ENT-team-member.preferred_language |
| Available languages | dropdown options | Yes | Active supported locales available to provider users | Inactive and Preparation locales hidden (REQ-021-076) | ENT-locale.english_name, ENT-locale.native_name |
| Save/apply action | button or auto-apply | Yes | Applies selected language to dashboard session and profile preference | Must persist preference before refresh/re-render (REQ-021-116) | no graph field (control) |

**Business Rules**:

- Bundle loading for the Provider Dashboard follows General Module Rule 14.
- Language selection applies to dashboard UI, system labels, validation messages, and provider-facing system notifications where FR-030 templates exist. (REQ-021-066)
- See REQ-021-003 and REQ-021-025.
- See REQ-021-013.
- If a provider's selected locale becomes inactive, the dashboard falls back to the configured fallback locale. (REQ-021-067)

**Notes**:

- The language selector lives in the top bar near account/profile controls.
- The control should show readable language names and native names where space permits.
- Switching language should preserve the current route and user task where technically feasible.

---

### Admin Platform

#### Screen 3: Admin Platform - Top-Bar Language Selector

**Purpose**: Allow admin users to switch the Admin Platform interface language while preserving their current administrative context.

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules | Graph field |
| --- | --- | --- | --- | --- | --- |
| Current language | dropdown | Yes | Currently selected admin UI language | Must be an active supported locale | ENT-admin-user-account.preferred_language |
| Available languages | dropdown options | Yes | Active supported locales available to admin users | Inactive and Preparation locales hidden (REQ-021-076) | ENT-locale.english_name, ENT-locale.native_name |
| Apply action | button or auto-apply | Yes | Applies selected language to admin session and preference | Must persist preference (REQ-021-117) | no graph field (control) |

**Business Rules**:

- Bundle loading for the Admin Platform follows General Module Rule 14.
- Localization-management screens may show translation values in multiple languages at once, regardless of the admin user's current UI language. (REQ-021-069)
- Admin UI language preference does not change the default locale of the translation registry. (REQ-021-070)
- Draft translation changes are visible inside localization-management screens but are not used to localize the Admin Platform UI until published. (REQ-021-071)

**Notes**:

- The language selector lives in the top bar near profile/session controls.
- Admin screens that compare locale values should keep column language labels visible even when the admin UI language changes.

---

#### Screen 4: Admin - Localization Dashboard & Language Management

**Purpose**: Provide the overall localization dashboard where Admin manages available system languages and sees release readiness across tenants.

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules | Graph field |
| --- | --- | --- | --- | --- | --- |
| Language list | table | Yes | All supported locales/languages in the system | Includes active, inactive, default, and preparation-only locales | ENT-locale.code, ENT-locale.english_name, ENT-locale.native_name, ENT-locale.direction, ENT-locale.status, ENT-locale.is_default |
| Locale code | text | Yes | Locale identifier such as `en`, `tr`, `en-GB`, or `ar` | Must be unique; must follow supported locale-code format (REQ-021-077) | ENT-locale.code |
| English name | text | Yes | Locale name in English | Required | ENT-locale.english_name |
| Native name | text | Yes | Locale name in native script/language | Required | ENT-locale.native_name |
| Direction | badge/select | Yes | Text direction metadata | Allowed values: `ltr`, `rtl` | ENT-locale.direction |
| Status | badge/toggle | Yes | Active, Inactive, or Preparation | The default locale must be Active (REQ-021-078); moving a locale from Preparation to Active is Super Admin only and needs a published bundle for every surface (REQ-021-125) | ENT-locale.status |
| Default locale | badge/radio | Yes | Identifies the default locale | Exactly one default locale, which must be Active; changing it is Super Admin only (REQ-021-078, REQ-021-049) | ENT-locale.is_default |
| Tenant coverage | metric group | No | Patient, Provider, and Admin coverage percentages | System-generated | ENT-locale.coverage_by_surface |
| Last published version | read-only text | No | Current active version by language/surface | System-generated | ENT-locale.last_published_version |
| Add language action | button | Yes | Opens add-language form/modal | Locale code must be unique (REQ-021-077) | no graph field (control) |
| Remove/deactivate action | button | Conditional | Deactivates or removes a language from active use | Default locale cannot be removed; historical data preserved (REQ-021-078, REQ-021-072) | no graph field (control) |

**Business Rules**:

- This is the admin landing screen for localization.
- Admin can add new languages/locales from this screen.
- Admin can deactivate languages; deactivation hides the language from user-facing selectors but preserves translations, versions, and audit history. (REQ-021-072)
- Hard deletion of a language is not allowed once translation history or published versions exist; use Inactive state instead. (REQ-021-073)
- English (`en`) is always the source locale and is the initial default locale; only the default locale can be changed, and only by a Super Admin. (REQ-021-074)
- New languages start in Preparation state and become Active only under REQ-021-125: Super Admin only, with a published bundle for every surface (Patient App, Provider Dashboard, Admin Platform). (REQ-021-075)
- Only Active locales appear in the Patient, Provider, and Admin interface-language selectors; Inactive and Preparation locales are hidden from them. The spoken-language and notification-template language lists used by FR-032 and FR-030 show Active and Preparation locales. (REQ-021-076, REQ-021-025)
- Selecting a language row opens Screen 5: Admin - Language Detail.

**Notes**:

- This screen should be the designer's primary overview for localization health.
- Coverage should be shown by tenant because Patient, Provider, and Admin readiness can differ.
- The default language should be visually protected from normal remove/deactivate controls.

---

#### Screen 5: Admin - Language Detail

**Purpose**: Let Admin manage one language's translations, coverage, draft changes, import route, edit route, export route, and publish readiness.

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules | Graph field |
| --- | --- | --- | --- | --- | --- |
| Language header | read-only group | Yes | Locale code, English name, native name, direction, status | Sourced from supported locale catalog | ENT-locale.code, ENT-locale.english_name, ENT-locale.native_name, ENT-locale.direction, ENT-locale.status |
| Tenant coverage | metric group | Yes | Patient, Provider, and Admin coverage for this language | System-generated | ENT-locale.coverage_by_surface |
| Pending draft changes | read-only metric/list | No | Count and entry points for pending changes | System-generated | ENT-locale.pending_draft_count |
| Missing keys | read-only metric/link | No | Missing translations for this language | Links to filtered key editor/inventory | ENT-locale.missing_key_count |
| Review-needed keys | read-only metric/link | No | Translations requiring review after source changes | Links to filtered key editor/inventory | ENT-locale.review_needed_count |
| Fallback locale | select | No | The locale shown when this language has no value for a key; English is always the last resort after it | Must be a supported locale other than this language; not offered for English (REQ-021-037) | ENT-locale.fallback_order |
| Edit keys route | action card/button | Yes | Opens Screen 6 filtered to this language | Must preserve selected language context | no graph field (control) |
| Import JSON route | action card/button | Yes | Opens Screen 8 for this language | Must preserve selected language context | no graph field (control) |
| Export JSON action | button | No | Exports this language by tenant/surface/group/version | Must identify draft vs published export (REQ-021-081) | no graph field (control) |
| Version history route | action card/button | Yes | Opens Screen 9 filtered to this language | Must preserve selected language context | no graph field (control) |
| Machine translation route | action card/button | Conditional | Opens Screen 10 for this language | Available only for non-English target languages and only to an admin holding the Manage Localization permission (REQ-021-079, REQ-021-121) | no graph field (control) |

**Business Rules**:

- Language Detail is the primary working screen for one language.
- Admin has two main update routes from this screen: edit individual keys or import JSON.
- Admin can also open machine translation for non-English languages when provider credentials and the Manage Localization permission are available. (REQ-021-079)
- Admin sets the language's fallback locale here; a missing value resolves to the selected language, then its fallback locale, then the English source locale. (REQ-021-037)
- Export is available for translator handoff, backup, and implementation review, but export does not modify system state. (REQ-021-080)
- Draft changes remain draft until published through Screen 9 or through controlled Import and Publish from Screen 8. (REQ-021-008)
- Language status changes should be made from Screen 4 unless the design chooses to surface the same controls here as secondary actions.

**Notes**:

- This screen should make it obvious whether the language is live, inactive, or still being prepared.
- For a new language rollout, Admin should be able to move from this screen to key editing, import, export, coverage checks, and version publishing without returning to the dashboard.

---

#### Screen 6: Admin - Translation Key Inventory

**Purpose**: List translation keys across the whole system and split the inventory into Patient, Provider, and Admin tenant sub-screens so design, development, and Admin can understand the localization map and open key-level editing.

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules | Graph field |
| --- | --- | --- | --- | --- | --- |
| Tenant sub-screen | tabs/segmented control | Yes | Patient App, Provider Dashboard, Admin Platform | Exactly one tenant selected | ENT-translation-key.surface |
| Selected language filter | select/read-only | No | Optional language filter, especially when opened from Language Detail | Must be a supported locale | ENT-locale.code |
| Namespace/group | table column/filter | Yes | Logical key group | Must follow key naming convention | ENT-translation-key.group_namespace |
| Key pattern / key | table column | Yes | Stable key identifier or starter key pattern | Must be stable and machine-readable | ENT-translation-key.key |
| Screen/context | table column | No | Product surface where key appears | Recommended for design/dev setup | ENT-translation-key.screen_context |
| English source value | table column | Conditional | Canonical source text for implemented keys | Required for active keys | ENT-translation-key.source_value |
| Selected-language value | table column | Conditional | Value for selected language when a language filter is applied | Must preserve placeholders and ICU syntax | ENT-translation-value.draft_value |
| Coverage/status | badge/filter | Yes | Published, Draft, Pending Publish, Missing, Review Needed, Deprecated, Orphaned | System-controlled where possible | ENT-translation-key.status |
| Source value owner | table column | No | Owning module/FR/team | Recommended | ENT-translation-key.source_value_owner |
| Required at launch | badge | Yes | Required or Optional | Must be reviewable before release | ENT-translation-key.required_at_launch |
| Flexibility status | badge | Yes | Baseline, implementation-discovered, deprecated, future | System/design governance field | ENT-translation-key.flexibility_status |
| Open key action | row click/button | Yes | Opens Screen 7 for the selected key | Must preserve tenant and selected language context where available | no graph field (control) |

**Business Rules**:

- This inventory is the canonical entry point for browsing and opening translation keys.
- Selecting a key opens Screen 7: Admin - Translation Key Detail Editor.
- This inventory is a baseline key map for design/dev setup, not a frozen exhaustive list.
- Developers may add, remove, split, or rename implementation keys without first updating this PRD when the change stays within the documented localization model, follows naming conventions, and is captured in the implementation registry/audit trail. (REQ-021-082)
- PRD/design updates are required only when key changes alter user-facing workflow scope, add a new screen/surface, change source-locale governance, or change publish/version/rollback behavior. (REQ-021-082)
- Shared/common keys may be reused only when meaning and context are identical across tenants. (REQ-021-083)
- Tenant-specific keys should remain tenant-scoped even when the English words are similar but the user context differs. (REQ-021-083)
- Admin-authored library text (treatment type descriptions and technique specifications) is registered here as key groups so it is translated through the registry. Provider-authored package names and descriptions are free text under General Module Rule 15, not keys. (REQ-021-127)

**Notes**:

- When opened from Language Detail, this screen should be pre-filtered to that selected language and optionally to Missing / Review Needed / Draft states.
- Designers should use this screen to understand key groups and tenant coverage, not to hand-place every final implementation key.
- Dev should treat the lists below as seed groups and examples; the live registry remains the operational source of truth.

##### Screen 6A: Patient App Key Inventory

**Baseline Key Groups**:

| Namespace / Key Pattern | Context | Starter Keys / Examples | Flexibility Notes |
| --- | --- | --- | --- |
| `common.*` | Shared patient UI actions and states | `common.save`, `common.cancel`, `common.continue`, `common.back`, `common.loading`, `common.error.generic` | Can expand as shared components mature |
| `auth.*` | Login, signup, email verification, password reset | `auth.login.title`, `auth.login.button`, `auth.register.title`, `auth.password_reset.title`, `auth.email_verification.message` | Exact auth keys may follow FR-001 implementation naming |
| `settings.language.*` | Patient Settings language controls | `settings.language.title`, `settings.language.selected`, `settings.language.fallback_notice` | Required for FR-021 patient language setting |
| `profile.*` | Patient profile and account settings | `profile.photo.add`, `profile.location.label`, `profile.phone.label`, `profile.preferences.title` | Keep medical/private data out of translation bundles |
| `inquiry.*` | Quote request / inquiry creation | `inquiry.destination.title`, `inquiry.concern.title`, `inquiry.medical_questionnaire.title`, `inquiry.submit.button` | Exact keys depend on FR-003/FR-025 screen implementation |
| `quote.*` | Offers, quote comparison, quote detail | `quote.list.title`, `quote.offer_count`, `quote.accept.button`, `quote.details.title` | Align with FR-004/FR-005 labels |
| `booking.*` | Booking/scheduling status and date selection | `booking.title`, `booking.date_range.label`, `booking.status.pending`, `booking.status.confirmed` | Align with FR-006 |
| `payment.*` | Payment progress, methods, receipts | `payment.progress.title`, `payment.method.title`, `payment.pay_now`, `payment.receipt.title` | Align with FR-007/FR-007b |
| `travel.*` | Travel logistics and itinerary display | `travel.itinerary.title`, `travel.flight.label`, `travel.hotel.label`, `travel.passport.notice` | Align with FR-008 |
| `treatment_library.*` | Admin-authored treatment type descriptions and technique specifications shown to patients | `treatment_library.type.description`, `treatment_library.technique.specification` | Library content is owned by FR-024; the text is translated through this registry (REQ-021-127) |
| `treatment.*` | In-progress treatment and treatment plan | `treatment.plan.title`, `treatment.day.label`, `treatment.status.in_progress`, `treatment.aftercare.start` | Align with FR-010 |
| `aftercare.*` | Aftercare tasks, questionnaires, education | `aftercare.today.title`, `aftercare.task.complete`, `aftercare.questionnaire.title`, `aftercare.resources.title` | Align with FR-010/FR-011 |
| `notifications.*` | Patient notification center labels | `notifications.title`, `notifications.empty`, `notifications.mark_all_read` | Notification content/templates remain owned by FR-030 |
| `support.*` | Help/support access | `support.help_center.title`, `support.ticket.create`, `support.contact.title` | Align with FR-035/FR-034 surfaces |

##### Screen 6B: Provider Dashboard Key Inventory

**Baseline Key Groups**:

| Namespace / Key Pattern | Context | Starter Keys / Examples | Flexibility Notes |
| --- | --- | --- | --- |
| `common.*` | Shared provider UI actions and states | `common.save`, `common.cancel`, `common.search`, `common.filter`, `common.empty_state` | Can share only where meaning is identical |
| `provider.nav.*` | Provider dashboard navigation/top bar | `provider.nav.dashboard`, `provider.nav.patients`, `provider.nav.quotes`, `provider.nav.settings`, `provider.nav.language` | Required for provider language selector |
| `provider.auth.*` | Provider login/account access | `provider.auth.login.title`, `provider.auth.password_reset.title` | May reuse auth concepts but tenant-scoped context can differ |
| `provider.patients.*` | Patient overview/work queue | `provider.patients.list.title`, `provider.patients.status`, `provider.patients.open_case` | Align with FR-009 |
| `provider.quotes.*` | Quote requests and quote submission | `provider.quotes.requests.title`, `provider.quotes.create.button`, `provider.quotes.submit.button` | Align with FR-003/FR-004 provider surfaces |
| `provider.bookings.*` | Provider booking schedule | `provider.bookings.title`, `provider.bookings.date`, `provider.bookings.status` | Align with FR-006 |
| `provider.treatment_library.*` | Admin-authored treatment type descriptions and technique specifications shown to providers | `provider.treatment_library.type.description`, `provider.treatment_library.technique.specification` | Library content is owned by FR-024; the text is translated through this registry (REQ-021-127) |
| `provider.treatment.*` | Treatment plan/execution participation | `provider.treatment.plan.title`, `provider.treatment.day.update`, `provider.treatment.status` | Align with FR-010 |
| `provider.analytics.*` | Provider analytics/reporting | `provider.analytics.title`, `provider.analytics.revenue`, `provider.analytics.conversion` | Align with FR-014 |
| `provider.finance.*` | Financial management and payouts | `provider.finance.payouts.title`, `provider.finance.earnings.title`, `provider.finance.statement.title` | Align with FR-017/FR-029/FR-032 as applicable |
| `provider.profile.*` | Provider profile settings | `provider.profile.languages.title`, `provider.profile.awards.title`, `provider.profile.logo.upload` | Spoken languages are profile data, not UI language preference |
| `provider.reviews.*` | Provider reviews tab/response | `provider.reviews.title`, `provider.reviews.respond`, `provider.reviews.empty` | Align with FR-013/FR-032 |
| `provider.support.*` | Provider help/support/settings support | `provider.support.help_center`, `provider.support.contact`, `provider.support.status` | Align with FR-032/FR-033/FR-034 |

##### Screen 6C: Admin Platform Key Inventory

**Baseline Key Groups**:

| Namespace / Key Pattern | Context | Starter Keys / Examples | Flexibility Notes |
| --- | --- | --- | --- |
| `common.*` | Shared admin UI actions and states | `common.save`, `common.cancel`, `common.search`, `common.filter`, `common.export`, `common.publish` | Can share with other tenants only when context is identical |
| `admin.nav.*` | Admin navigation/top bar | `admin.nav.dashboard`, `admin.nav.patients`, `admin.nav.providers`, `admin.nav.settings`, `admin.nav.language` | Required for admin language selector |
| `admin.auth.*` | Admin login/access management | `admin.auth.login.title`, `admin.auth.mfa.title`, `admin.auth.session_expired` | Align with FR-031 |
| `admin.patients.*` | Patient management | `admin.patients.list.title`, `admin.patients.detail.title`, `admin.patients.status` | Align with FR-016 |
| `admin.providers.*` | Provider management | `admin.providers.list.title`, `admin.providers.detail.title`, `admin.providers.languages.label` | Align with FR-015 |
| `admin.inquiries.*` | Inquiry/quote oversight | `admin.inquiries.list.title`, `admin.inquiries.detail.title`, `admin.inquiries.status` | Align with FR-003/FR-004 |
| `admin.payments.*` | Payment/billing/finance admin | `admin.payments.dashboard.title`, `admin.payments.refund.action`, `admin.payouts.title` | Align with FR-007/FR-017/FR-029 |
| `admin.reviews.*` | Review management | `admin.reviews.title`, `admin.reviews.insert`, `admin.reviews.remove`, `admin.reviews.takedown_queue` | Align with FR-013 |
| `admin.promotions.*` | Promotions/referrals | `admin.promotions.title`, `admin.promotions.create`, `admin.promotions.status` | Align with FR-019/FR-020 |
| `admin.localization.*` | FR-021 localization management | `admin.localization.dashboard.title`, `admin.localization.language.add`, `admin.localization.import.title`, `admin.localization.version.rollback` | Core FR-021 admin keys |
| `admin.notifications.*` | Notification rules/config | `admin.notifications.rules.title`, `admin.notifications.template.title`, `admin.notifications.preview` | Align with FR-030; content/template body remains FR-030-owned |
| `admin.help_center.*` | Help centre/content management | `admin.help_center.faq.title`, `admin.help_center.article.title`, `admin.help_center.video.title` | Align with FR-033 |
| `admin.support.*` | Support center ticketing | `admin.support.tickets.title`, `admin.support.status`, `admin.support.assignment` | Align with FR-034 |
| `admin.audit.*` | Audit trail and security settings | `admin.audit.title`, `admin.audit.actor`, `admin.audit.outcome` | Align with FR-031 |

---

#### Screen 7: Admin - Translation Key Detail Editor

**Purpose**: Let Admin open one selected translation key from the inventory, review all language values for that key, and edit per-language values through a controlled draft workflow.

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules | Graph field |
| --- | --- | --- | --- | --- | --- |
| Translation key | read-only text | Yes | Stable key identifier such as `auth.login.title` | Editable only through controlled key lifecycle process | ENT-translation-key.key |
| Tenant/surface | read-only/select | Yes | Patient App, Provider Dashboard, Admin Platform | Required | ENT-translation-key.surface |
| Group/namespace | read-only/select | Yes | Logical namespace | Required | ENT-translation-key.group_namespace |
| Screen/context | text | No | Where the key appears and how it is used | Recommended for translator clarity | ENT-translation-key.screen_context |
| Description/context | textarea | No | Translator guidance and usage context | Recommended | ENT-translation-key.description |
| English source value | textarea | Yes | Canonical source value | Source edit is Super Admin only and requires a reason and placeholder validation (REQ-021-020) | ENT-translation-key.source_value |
| Locale values | textarea per active language | Conditional | Translation value for each active language | Must preserve placeholders and ICU syntax | ENT-translation-value.draft_value |
| Selected language highlight | read-only state | No | Highlights the language filter used when opened from Language Detail | Must not hide other active language values | no graph field (display state) |
| Character guidance | read-only text | No | Optional display length guidance for constrained UI | Non-blocking unless a screen-specific limit exists (REQ-021-088) | ENT-translation-key.length_guidance |
| Non-semantic change confirmation | checkbox | No | Shown in the English source edit dialog only; Super Admin confirms the edit does not change the meaning | When checked and the edit passes validation, dependent locale values are not marked Review Needed (REQ-021-020) | no graph field (control) |
| Change reason | textarea | Conditional | Required when editing English source and on every publish | Required for English source edits and for every publish (REQ-021-087) | ENT-translation-audit-log.reason |
| History panel | read-only log | No | Prior changes, imports, publishes, and rollback references | System-generated | ENT-translation-audit-log.action, ENT-translation-audit-log.reference |
| Accept as reviewed action | button | Conditional | Per locale value: clears Review Needed without changing the value | Shown only on values marked Review Needed; recorded in the audit history (REQ-021-105) | no graph field (control) |
| Save draft action | button | Yes | Saves edited values as draft | Does not affect runtime bundles | no graph field (control) |

**Business Rules**:

- This screen is downstream from Screen 6: Translation Key Inventory.
- One key is shown at a time.
- All active language values for the selected key should be visible or accessible from this screen. (REQ-021-084)
- See REQ-021-008.
- Admin can save one language value or multiple language values for the key.
- System must block saving if placeholders are removed, renamed, or malformed. (REQ-021-085)
- See REQ-021-020. Review Needed marking of dependent locale values happens only after the English edit passes validation; a rejected edit marks nothing.
- A Review Needed value is cleared when Admin saves a reviewed value or selects Accept as reviewed. (REQ-021-105)

**Notes**:

- Show English source value first, then active languages, then inactive/preparation languages if Admin chooses to include them.
- Show missing/review-needed indicators beside affected languages.
- Show a clear Pending Publish state after saving draft changes.

---

#### Screen 8: Admin - JSON Import Modal/Screen

**Purpose**: Allow Admin to upload a JSON translation package for one language, tenant/surface, and group; validate it; then choose Import as Draft or controlled Import and Publish Version.

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules | Graph field |
| --- | --- | --- | --- | --- | --- |
| Target language | select/read-only | Yes | Language receiving imported values | Must be supported; inactive/preparation languages allowed for preparation workflows; importing into the English source locale is an English source edit (REQ-021-123) | ENT-translation-import.locale |
| Tenant/surface | select | Yes | Target translation surface | Patient App, Provider Dashboard, Admin Platform | ENT-translation-import.surface |
| Group/namespace | select | Yes | Target key group | Must exist or be authorized for creation (REQ-021-094) | ENT-translation-import.group_namespace |
| File | upload | Yes | JSON translation file/package | Valid JSON; size limit configured by platform | ENT-translation-import.file_name |
| Import mode | radio/select | Yes | Overwrite draft values or only add missing | Must be selected before confirmation | ENT-translation-import.mode |
| Validation preview | read-only panel | Yes | Shows created, updated, unchanged, skipped, row warnings, and errors | Required before import confirmation (REQ-021-090, REQ-021-095) | ENT-translation-import.summary_counts, ENT-translation-import.validation_result |
| Import decision | radio/select | Yes | Import as Draft or Import and Publish Version | Import and Publish disabled if validation errors exist, if any row is skipped for an error, or if approval is required (REQ-021-095) | ENT-translation-import.decision |
| Publish summary | textarea | Conditional | Required when choosing Import and Publish Version | Required before publish confirmation | ENT-translation-import.publish_summary |
| Error report | download link | Conditional | Downloadable validation errors/warnings | Shown when validation issues exist | ENT-translation-import.error_report |

**Business Rules**:

- JSON import must be a separate modal/screen from the key editor.
- See REQ-021-036.
- Import preview is required before confirmed import. (REQ-021-090)
- System must validate JSON syntax, known keys, duplicate keys, placeholder consistency, ICU syntax, target-locale compatibility, and unsupported/orphaned keys. (REQ-021-091)
- Every confirmed import creates an import record with file name, actor, timestamp, language, surface, group, decision, summary counts, and validation results. (REQ-021-092)
- If Admin chooses Import and Publish Version, system creates both an import record and an immutable published version record. (REQ-021-093)
- Unknown keys are blocked unless Admin has explicit permission to create new registry keys through import. A new key created through import must carry an English value in the same file; a row without one is an error. (REQ-021-094)
- An import into the English source locale is an English source edit: it is Super Admin only and follows the REQ-021-020 controls (reason, audit, Review Needed marking after validation). (REQ-021-123)
- When any row is skipped for an error, only Import as Draft is offered; publishing is a separate later action from Screen 9. (REQ-021-095)

**Notes**:

- Import summary should separate structural errors, row-level warnings, publish-blocking errors, and non-blocking warnings.
- The modal/screen should clearly show whether the file is only being imported as draft or is being published as a live version.

---

#### Screen 9: Admin - Language Version History & Rollback

**Purpose**: Manage published versions for a language, inspect changes, publish draft changes, and roll back to a prior version.

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules | Graph field |
| --- | --- | --- | --- | --- | --- |
| Version ID | read-only text | Yes | Published bundle identifier | System-generated | ENT-translation-version.version_id |
| Language | filter/read-only | Yes | Language included in version | Required | ENT-translation-version.locale |
| Tenant/surface | filter/read-only | Yes | Surface included in version | Required | ENT-translation-version.surface |
| Group/namespace | filter/read-only | No | Group included in version | Required when publishing partial bundle | ENT-translation-version.group_namespace |
| Source type | badge | Yes | Manual patch, JSON import, import+publish, machine translation, rollback | System-generated | ENT-translation-version.source_type |
| Change summary | textarea/read-only | Yes | Human-readable reason for publish or rollback | Required for publish/rollback (REQ-021-102) | ENT-translation-version.change_summary |
| Pending changes | read-only list | No | Draft keys ready to publish | System-generated | ENT-translation-value.status |
| Coverage summary | read-only panel | No | Translation coverage and missing key count | System-generated | ENT-translation-version.coverage_summary |
| Validation status | read-only badge | Yes | Pass, warning, blocked | Blocking errors prevent publish | ENT-translation-version.validation_status |
| Review Needed count | read-only metric | No | Number of values still marked Review Needed in the selected scope | System-generated; shown in the publish confirmation; does not block publish (REQ-021-124) | ENT-locale.review_needed_count |
| Publish action | button | Conditional | Creates a new published version from draft changes | Super Admin only; enabled only after validation (REQ-021-051, REQ-021-099) | no graph field (control) |
| Rollback action | button | Conditional | Restores selected prior bundle as active via new rollback version | Super Admin only; requires reason and confirmation (REQ-021-051, REQ-021-100) | no graph field (control) |
| Compare versions action | button | No | Compares two versions at key/value level | Versions must share language/surface scope (REQ-021-101) | no graph field (control) |

**Business Rules**:

- See REQ-021-045.
- Publishing creates a new active bundle version for selected language, tenant/surface, and group scope. (REQ-021-096)
- See REQ-021-012 and REQ-021-045.
- Cache invalidation occurs after publish and rollback. (REQ-021-097)
- System must record actor, timestamp, publish/rollback reason, impacted keys, language, tenant/surface, and previous active version. (REQ-021-098)
- Admin cannot publish if required validation errors exist, such as malformed ICU syntax or placeholder mismatch. (REQ-021-099)
- Review Needed values do not block publish; the publish confirmation shows how many remain flagged. (REQ-021-124)

**Notes**:

- Version history should show whether a version came from individual text patching, JSON import, import+publish, or rollback.
- This screen is language-focused when entered from Language Detail, but can support filters for all languages if the dashboard needs a global history view.

---

#### Screen 10: Admin - Machine Translation Provider & Draft Generation

**Purpose**: Let Admin configure a machine-translation provider API key and generate review-required draft translations for a selected non-English language.

**Data Fields**:

| Field Name | Type | Required | Description | Validation Rules | Graph field |
| --- | --- | --- | --- | --- | --- |
| Provider | select | Yes | Machine-translation service used for draft generation | Options may include Google Cloud Translation, DeepL, Microsoft Azure Translator, and Amazon Translate; custom provider allowed only if integration exists (REQ-021-108) | ENT-mt-provider-credential.provider, ENT-mt-job.provider |
| Provider status | badge/read-only | Yes | Connected, Not Configured, Error, or Disabled | System-generated from the credential, the connection check, and the Enable/Disable control (REQ-021-109) | ENT-mt-provider-credential.status |
| Enable/Disable provider | toggle | Yes | Turns the selected provider on or off for draft generation | A Disabled provider cannot start a job; Enable verifies the connection again (REQ-021-109) | no graph field (control) |
| API key / credential | secret input | Conditional | Credential used to call the selected provider | Required to enable provider; encrypted at rest; masked after save (REQ-021-031) | ENT-mt-provider-credential.credential_ref |
| Supported languages | read-only/list | No | Provider-supported target languages available to Admin | Retrieved from provider metadata or configured integration | ENT-mt-provider-credential.supported_languages |
| Target language | select | Yes | Non-English language receiving machine-generated draft values | Must be supported by FR-021 locale catalog and selected provider; English/source locale blocked (REQ-021-104) | ENT-mt-job.target_locale |
| Tenant/surface scope | multi-select | Yes | Patient App, Provider Dashboard, Admin Platform | Default all selected surfaces for the target language | ENT-mt-job.surface_scope |
| Group/namespace scope | multi-select | No | Optional key groups to include | Blank means all groups for selected surfaces | ENT-mt-job.group_scope |
| Generation mode | radio/select | Yes | Prefill Missing Keys or Replace Entire Language | Replace Entire Language disabled for English/source locale (REQ-021-104) | ENT-mt-job.generation_mode |
| Preview counts | read-only panel | Yes | Shows eligible, skipped, missing, replacement, error, and estimated usage counts | Required before generation confirmation | ENT-mt-job.preview_counts |
| Confirmation reason | textarea | Yes | Business reason for running machine translation | Required for audit | ENT-mt-job.reason |
| Generate draft action | button | Yes | Starts machine-translation job and saves accepted results as draft | Requires a Connected and enabled provider, preview, confirmation, and the Manage Localization permission (REQ-021-110) | no graph field (control) |
| Free-text translation switch | toggle | Yes | Platform-wide switch for translating free text written by one user for another | Off by default; one platform-wide setting; uses the active machine-translation provider (REQ-021-119) | no graph field (setting SET-free-text-translation-enabled) |
| Free-text translation monthly budget | number | Yes | Monthly spending cap for free-text translation | No default figure; when the monthly limit is reached free text is shown untranslated (REQ-021-120) | no graph field (setting SET-free-text-translation-monthly-budget) |
| Job history | table | No | Prior machine-translation jobs, actor, language, mode, counts, provider, status (Queued, Running, Completed, Partially failed, or Failed), and errors | System-generated (REQ-021-111) | ENT-mt-job.job_id, ENT-mt-job.actor_id, ENT-mt-job.target_locale, ENT-mt-job.generation_mode, ENT-mt-job.counts, ENT-mt-job.provider, ENT-mt-job.status, ENT-mt-job.error_summary |

**Business Rules**:

- Machine translation of system-controlled text is a draft-generation tool, not a runtime translation path. Free-text translation for the reader is the separate case in General Module Rule 15. (REQ-021-103)
- Only an admin holding the Manage Localization permission can use the machine-translation route. (REQ-021-121)
- A provider that fails the connection check is set to Error and no job starts; a Disabled provider cannot start a job. (REQ-021-109)
- Job status is one of Queued, Running, Completed, Partially failed, or Failed. (REQ-021-111)
- The Free-text translation panel on this screen holds the platform switch and the monthly budget for translating free text written by one user for another. It uses the active machine-translation provider configured on this screen. No other behaviour is added here. (REQ-021-119, REQ-021-120)
- Machine translation can only target non-English locales; English/source values remain human-authored and governed by source-edit protections. (REQ-021-104)
- See REQ-021-028.
- Replace Entire Language generates replacement draft values for all selected target-language keys in the selected scope, except protected source values. (REQ-021-029)
- All machine-generated values are marked Review Needed until Admin saves a reviewed value or selects Accept as reviewed on Screen 7. (REQ-021-105)
- Generated values must pass the same placeholder, ICU syntax, key-existence, target-locale compatibility, and publish validation rules as JSON imports. (REQ-021-106)
- Machine translation for translation drafts must not process patient/provider messages, reviews, support-ticket messages, notes, uploaded documents, legal content, or other user-generated/private content unless the owning FR explicitly permits it. Free-text translation for the reader (General Module Rule 15) is a separate case. (REQ-021-030)
- API credentials must be encrypted at rest, masked in UI after save, and never exported in JSON files or audit detail. (REQ-021-031)
- Every provider configuration change and machine-translation job must be audited with actor, timestamp, provider, target language, mode, scope, counts, and reason. (REQ-021-107)

**Notes**:

- Notable starting providers for Admin evaluation: Google Cloud Translation, DeepL, Microsoft Azure Translator, and Amazon Translate.
- The screen should show cost/usage warnings where provider metadata or integration limits are available.
- Machine translation should be treated as a way to accelerate whole-language readiness, not as key-by-key silent automation.

---

## Business Rules

### General Module Rules

- **Rule 1**: All user-facing system-controlled text must be externalized into translation keys before production release. (REQ-021-032)
- **Rule 2**: Translation keys must be stable identifiers and should not be based on mutable display copy. (REQ-021-033)
- **Rule 3**: Active keys require an English source value. (REQ-021-034)
- **Rule 4**: Keys must include tenant/surface and group/namespace metadata. (REQ-021-035)
- **Rule 5**: Inline text edits save draft changes only; JSON imports default to Import as Draft, with Import and Publish Version allowed only when no row was skipped for an error, after full validation preview, publish-summary entry, and Super Admin authorization. When any row is skipped for an error, only Import as Draft is offered. (REQ-021-036, REQ-021-095)
- **Rule 6**: See REQ-021-013.
- **Rule 7**: See REQ-021-011 and REQ-021-096.
- **Rule 8**: See REQ-021-012 and REQ-021-045.
- **Rule 9**: Fallback applies per key: the selected locale first, then that locale's configured fallback locale, then always the English source locale. (REQ-021-037)
- **Rule 10**: Locale direction metadata must be stored so future RTL support is not blocked. (REQ-021-038)
- **Rule 11**: Machine-generated translations save as draft only, must be marked Review Needed, and cannot be served to runtime clients until published. (REQ-021-039)
- **Rule 12**: Machine translation generation can target a whole non-English language by missing keys or full-language replacement scope; the English source locale is never replaced by machine translation. (REQ-021-040)
- **Rule 13**: Clients MUST revalidate translation bundles against version metadata (ETag/hash or equivalent) on each fetch cycle. After a publish or rollback, the maximum acceptable stale window is a platform-configurable interval, recommended at 5 minutes or less, ensuring clients do not serve outdated bundles for an indeterminate period after a version change. (REQ-021-041)
- **Rule 14**: Each runtime surface loads the latest published bundle for the user's selected locale and for its own surface: the Patient App loads the patient-app bundle, the Provider Dashboard the provider-dashboard bundle, and the Admin Platform the admin-platform bundle. (REQ-021-059)
- **Rule 15**: See REQ-021-119.
- **Rule 16**: See REQ-021-120.
- **Rule 17**: Provider and admin screens format dates and numbers by the selected locale. Provider screens use the provider timezone set in FR-032 (a value from the FR-026 GMT list); admin screens use the platform default timezone. Patient screens follow Screen 1. (REQ-021-126)

### Data & Privacy Rules

- **Privacy Rule 1**: Translation bundles must not include patient/provider private data or user-generated content. (REQ-021-022)
- **Privacy Rule 2**: Import/export files must contain system-controlled text only unless another owning FR explicitly permits additional metadata. (REQ-021-042)
- **Privacy Rule 3**: Machine translation requests for translation drafts must contain system-controlled source text only and must exclude private data, medical data, user-generated content, legal content, uploaded documents, and support messages unless explicitly permitted by the owning FR. Free-text translation for the reader (General Module Rule 15) is a separate case and is not covered by this rule. (REQ-021-030)
- **Audit Rule**: System must log locale changes, protected source edits, imports, publishes, rollbacks, and missing-translation events with actor, timestamp, scope, and reason where applicable. (REQ-021-043)
- **Data Retention Rule**: Published version history and audit trail must be retained according to platform audit-retention policy. (REQ-021-044)
- **Data Integrity Rule**: Published versions are immutable and must remain inspectable after rollback. (REQ-021-045)

### Admin Editability Rules

**Editable by Admin**: (REQ-021-046)

- Supported locales, native names, activation state, fallback order, and locale direction metadata.
- Translation values for non-source locales.
- Translation key metadata such as description/context and group where allowed.
- Draft translation changes and import confirmations. Publish and rollback are Super Admin only.
- Machine-translation provider credentials, provider activation state, and machine-translation draft generation jobs.
- The free-text translation switch (one platform-wide setting, off by default) and its monthly translation budget (no default figure). (REQ-021-119, REQ-021-120)
- Currency display configuration where already owned by A-09/S-02.

**Fixed in Codebase (Not Editable)**: (REQ-021-047)

- Locale formatting library behavior.
- Runtime bundle fetch protocol.
- Mandatory system keys required by application code.
- Notification variable contracts owned by FR-030.
- Security and audit-retention mechanisms.

**Configurable with Restrictions**:

- See REQ-021-020.
- Translation key identifiers after first publish require controlled migration rather than casual editing. (REQ-021-048)
- Default locale changes require approval by the Super Admin alone (no second approver); the new default locale must be Active, and English always remains the last-resort fallback. (REQ-021-049)
- Machine translation full-language replacement requires explicit confirmation because it can overwrite many target-language draft values. (REQ-021-029)
- Historical versions and audit records cannot be deleted through normal admin controls. (REQ-021-050)

**Elevated Authorization Definition**: For the purposes of FR-021, "elevated authorization" means the **Super Admin** role as defined in FR-031 (Admin Access Control & Permissions). Only Super Admin role holders may edit English source values (including by import into the English locale), change the default locale, publish translation versions, and perform rollback operations. These four protected operations cannot be delegated. Moving a locale from Preparation to Active is also Super Admin only (REQ-021-125). The exact per-operation permission scope must be aligned with FR-031 configuration at implementation time. (REQ-021-051)

**Manage Localization Permission**: In this PRD, "Admin" means an admin user holding the Manage Localization permission. The permission covers everyday localization work: editing non-English translation values, importing JSON as a draft, and generating machine-translation drafts. The Super Admin holds it and may grant it to another admin role in the FR-031 permission matrix. No role is added by this PRD. (REQ-021-122)

### Payment & Billing Rules

- **Currency Rule 1**: Currency display must use configured country/locale/currency rules without storing currency settings inside translation JSON files. (REQ-021-052)
- **Currency Rule 2**: Currency conversion source, refresh cadence, markup, rate locking, and payment-collection fallback are owned by FR-029 / S-02 and consumed by FR-021 for localized display. Locale-aware number formatting (decimal separator, symbol position, digit grouping, and RTL currency rendering) is owned by S-02 as a shared service capability and consumed by FR-021; neither FR-021 nor FR-029 duplicates this formatting logic. (REQ-021-053)
- **Currency Rule 3**: User-selected language does not automatically override timezone or currency unless product rules explicitly map country/locale defaults. (REQ-021-054)

### Integration & Ownership Rules

- **FR-026 / A-09 App Settings**: FR-021 owns language/locale catalog semantics; FR-026 may surface the catalog through the broader App Settings shell but must not become the language-list source of truth.
- **FR-030 / S-03 Notification Rules & Configuration**: FR-030 owns template authoring, variables, preview, channel content, and all notification wording; notification wording is not held in a translation bundle. FR-021 supplies the locale catalog and fallback order to FR-030. (REQ-021-115)
- **FR-027 / Legal Content Management**: FR-027 owns legal content versioning and acceptance (see FR-027 REQ-027-036 for the missing-localized-version fallback, and REQ-027-002 and REQ-027-029 for versioning); FR-021 supplies locale/fallback principles.
- **FR-024 / Treatment Package Management**: Admin-authored library text (treatment type descriptions and technique specifications) registers with FR-021 as key groups on Screens 6A and 6B. Provider-authored package names and descriptions are free text translated under General Module Rule 15, not registry keys. (REQ-021-127, REQ-021-119)
- **S-02 / Payment Processing Service**: Currency source, refresh cadence, rounding policy, and display formatting are configured/audited outside translation JSON.
- **FR-031 / Admin Access Control & Permissions**: FR-031 owns role definitions and the permission matrix; FR-021's four protected operations and the Preparation-to-Active locale change must be registered as Super Admin-only permissions, and the Manage Localization permission must be registered, in the FR-031 permission matrix at implementation time. The exact per-operation permission scope must be aligned with FR-031 configuration before release. (REQ-021-051)
- **Currency Rate Source**: Failure handling: Use last valid configured rate within allowed freshness window or show configured fallback per S-02/finance rules.
- **Translation Vendor / Translator Workflow**: Failure handling: Invalid or incomplete files remain draft and cannot publish when blocking validation errors exist.
- **Machine Translation Service**: Data format: Source text, target locale, placeholder/ICU metadata, and key context for system-controlled strings only. Error handling: Save job errors and partial counts; do not create publishable values for failed rows. Failure handling: Provider errors, quota limits, unsupported languages, placeholder mismatches, or malformed outputs are recorded in job history; accepted results remain draft and cannot publish until validation passes. (REQ-021-111)
- **Patient App bundle fetch**: Authentication: Uses existing app authentication/session rules where required. Error handling: Fall back to cached bundle or default locale where allowed. (REQ-021-114)
- **Provider Dashboard bundle fetch**: Authentication: Uses provider dashboard authentication. Error handling: See REQ-021-114.
- **Admin Platform localization management**: Error handling: Block publish on validation failures; preserve draft state for correction. (REQ-021-089, REQ-021-099) Protected endpoints (publish, rollback, English source edit, default locale change) must return HTTP 403 with the platform-standard error format when called by a non-Super-Admin role. (REQ-021-112)
- **Notification Service**: Authentication: Internal service integration. Error handling: Use the fallback locale template/content when recipient locale is missing; the locale catalog and fallback order come from FR-021 and the wording from FR-030 templates. (REQ-021-115)
- **Authentication**: Only authenticated admins holding the Manage Localization permission can access localization-management Screens 4 to 10; the Screen 3 language selector is open to every authenticated admin. (REQ-021-055)
- **Encryption**: Import/export files and bundle APIs must follow platform transport security requirements.
- **Threat mitigation**: Import validation must prevent malformed payloads, invalid placeholders, and oversized files from disrupting published bundles. (REQ-021-091)
- Missing translation events are logged immediately when detected by runtime fallback, import validation, registry validation, or publish validation. (REQ-021-016)
- Non-default locales may temporarily rely on fallback text when coverage is incomplete, provided release stakeholders accept that coverage state.

---

## Dependencies

- FR-026 / A-09 App Settings: may surface settings navigation and shared country/timezone/security configuration
- FR-030 / S-03 Notification Rules & Configuration: notification template language variants consume supported locales and fallback rules
- FR-027 / Legal Content Management: legal documents may have localized versions
- FR-024 / Treatment Package Management: admin-authored library text registers as key groups; provider-authored package names and descriptions are free text under General Module Rule 15
- FR-032 / Provider Dashboard Settings: provider profiles include spoken-language selections (Active and Preparation locales) and the provider timezone used by General Module Rule 17
- S-02 / Payment Processing Service: currency conversion and formatting are part of localization display
- FR-029 / S-02 Payment System Configuration: owns enabled currencies, currency pairs, conversion sources, markup, rate locking, and fallback-to-USD behavior
- FR-031 / Admin Access Control & Permissions: defines "elevated authorization" as the Super Admin role and holds the Manage Localization permission


---

## User Scenarios & Testing

### User Story 1 - Patient Selects Turkish (Priority: P1)

Patient changes language to Turkish in Patient App Settings and the Patient App uses the latest published Turkish patient-app bundle.

**Why this priority**: Patient-facing language selection is the core user outcome of FR-021.

**Independent Test**: Change a patient account language to Turkish and verify patient-app labels/messages render from the published Turkish bundle with fallback for missing keys.

**Acceptance Scenarios**:

1. **Given** Turkish is active and published for Patient App, **When** patient selects Turkish, **Then** navigation, buttons, validation messages, empty states, and system labels display in Turkish where translated.
2. **Given** a Patient App key is missing in Turkish, **When** patient views that screen, **Then** system displays configured fallback text and logs the missing key.
3. **Given** Turkish is deactivated after patient selected it, **When** patient next opens the app, **Then** system applies fallback behavior and does not show inactive Turkish as a selectable option.

---

### User Story 2 - Provider Switches Dashboard Language (Priority: P1)

Provider user changes dashboard UI language from the top bar without changing provider profile spoken-language data.

**Why this priority**: Provider dashboard localization is required across tenant surfaces and must not corrupt provider profile language data.

**Independent Test**: Change Provider Dashboard language from top bar and confirm UI text changes while profile spoken-language chips remain unchanged.

**Acceptance Scenarios**:

1. **Given** provider selects Turkish from the top bar, **When** the selection is applied, **Then** Provider Dashboard labels and validation messages render from the Turkish provider-dashboard bundle.
2. **Given** provider profile spoken languages include English and Turkish, **When** provider changes dashboard UI language, **Then** provider spoken-language chips are not overwritten.

---

### User Story 3 - Admin Edits One Translation Key (Priority: P1)

Admin corrects one translation value in the registry, saves it as draft, then publishes it.

**Why this priority**: Day-to-day translation corrections require a precise, controlled editing workflow.

**Independent Test**: Edit one locale value, verify it remains pending draft, publish it, and verify it appears in a new published version.

**Acceptance Scenarios**:

1. **Given** Admin edits a Turkish value, **When** Admin saves, **Then** the key is marked Pending Publish and runtime clients still use the previous published value.
2. **Given** Admin publishes pending Turkish Patient App changes, **When** Patient App fetches latest bundle, **Then** the new Turkish value appears.
3. **Given** a Super Admin edits the English source value, **When** the edit passes validation, **Then** system requires a reason and marks non-English translations for review, unless the Super Admin confirmed the edit as non-semantic. A rejected edit marks nothing.

---

### User Story 4 - Admin Imports Translator JSON (Priority: P1)

Admin exports source JSON, receives translated JSON, validates the package, then either imports it as draft for later review or imports and publishes it as a version.

**Why this priority**: Bulk translation is necessary when adding or maintaining a complete locale.

**Independent Test**: Export English source JSON, import translated Turkish JSON, review validation summary, confirm either Import as Draft or Import and Publish Version, and verify import/version history.

**Acceptance Scenarios**:

1. **Given** Admin uploads a valid Turkish JSON file, **When** validation completes, **Then** system shows created/updated/unchanged/skipped/error counts and publish-blocking status before import confirmation.
2. **Given** Admin chooses Import as Draft, **When** import succeeds, **Then** values are saved as draft, an import record is created, and runtime clients still receive the previous published bundle.
3. **Given** Admin chooses Import and Publish Version after a fully valid preview, **When** Admin enters a publish summary and confirms, **Then** system creates both an import record and a new immutable published version.
4. **Given** Import and Publish Version succeeds, **When** client fetches latest translation metadata, **Then** the new version is available.
5. **Given** an uploaded file has a row that must be skipped for an error, **When** Admin chooses to import valid rows only, **Then** only Import as Draft is offered and publishing is a separate later action.

---

### User Story 5 - Admin Rolls Back Translation Version (Priority: P1)

Admin restores a previous published translation bundle after a bad translation release.

**Why this priority**: Localization mistakes can affect all tenants and require safe recovery.

**Independent Test**: Publish a new version, roll back to a prior version, and verify active bundle content matches the prior version while history remains intact.

**Acceptance Scenarios**:

1. **Given** version `v3` is active and version `v2` was previously active, **When** Admin rolls back to `v2`, **Then** system creates rollback version `v4` containing `v2` bundle content.
2. **Given** rollback is confirmed, **When** clients revalidate translation metadata, **Then** clients receive the rollback version.
3. **Given** rollback occurred, **When** Admin views version history, **Then** `v2`, `v3`, and rollback `v4` remain visible with actor, timestamp, and reason.

---

### User Story 6 - Local Currency and Timezone Display (Priority: P2)

System displays prices and scheduled times in user-appropriate formats.

**Why this priority**: Currency and timezone localization improve comprehension and trust, but translation management is the higher-risk FR-021 workflow.

**Independent Test**: Set user timezone/country/locale context and verify appointment times and price formatting display correctly without changing canonical stored values.

**Acceptance Scenarios**:

1. **Given** user timezone is GMT+3 (a value from the FR-026 GMT list), **When** an appointment is stored as 09:00 UTC, **Then** user sees 12:00 with no daylight-saving shift.
2. **Given** user locale/country supports GBP display, **When** a quote price is shown, **Then** currency symbol/code and formatting match configured display rules.

---

### User Story 7 - Admin Generates Machine-Translated Drafts (Priority: P2)

Admin configures a machine-translation provider and uses it to prepare a non-English language for review.

**Why this priority**: Machine translation can accelerate whole-language readiness, but it must remain controlled and reviewable.

**Independent Test**: Configure a provider credential, run Prefill Missing Keys for Turkish, run Replace Entire Language for a non-English preparation locale, and verify generated values are draft-only, review-needed, audited, and publishable only through Screen 9.

**Acceptance Scenarios**:

1. **Given** no active provider credential exists, **When** Admin opens Machine Translation, **Then** system requires provider selection, API key entry, and successful connection verification before generation; if the connection fails the provider status becomes Error and no job starts. (REQ-021-109)
2. **Given** Turkish has missing keys, **When** Admin chooses Prefill Missing Keys, **Then** only missing Turkish values are machine-generated as Review Needed drafts.
3. **Given** Spanish is a preparation locale, **When** Admin chooses Replace Entire Language, **Then** all selected Spanish target-language values are replaced as machine-generated drafts while English source values remain unchanged.
4. **Given** machine-generated drafts exist, **When** runtime clients fetch published bundles, **Then** they continue receiving the previous published values until Admin publishes a new version.

### Edge Cases

- What happens when a selected locale is deactivated after users already selected it?
- What happens when a published bundle is missing a key needed by a runtime screen?
- How does system handle an import file with valid JSON but unknown keys?
- How does system handle placeholder mismatch between English source and translated value?
- What happens when English source copy changes meaning after non-English translations already exist?
- How does system prevent draft translation values from leaking to runtime clients?
- What happens when rollback occurs while clients have cached the newer bad version?
- How does system separate provider spoken-language profile data from provider UI language preference?
- What happens when machine translation provider credentials are invalid, quota-limited, or unavailable?
- What happens when machine translation output drops placeholders, breaks ICU syntax, or returns unsupported language content?
- How does system prevent Replace Entire Language from affecting English/source values?

---

## Functional Requirements Summary

### Core Requirements

- **REQ-021-001**: System MUST support multiple languages, initially English and Turkish, with expandable locale catalog and future RTL readiness.
- **REQ-021-002**: Patients MUST be able to select preferred language from Patient App Settings, and preference MUST persist across sessions/devices where account sync exists.
- **REQ-021-003**: Provider users MUST be able to select Provider Dashboard language from the dashboard top bar without overwriting provider profile spoken-language data.
- **REQ-021-004**: Admin users MUST be able to select Admin Platform language from the dashboard top bar.
- **REQ-021-005**: System MUST translate UI strings, validation messages, empty states, system labels, emails, and push notifications for supported locales where the owning module supplies translatable content.
- **REQ-021-006**: Admin MUST be able to manage supported locales, activation state, fallback order, native names, and locale direction metadata; only a Super Admin can change the default locale.
- **REQ-021-007**: Admin MUST be able to edit translation values in a table/grid registry and key-detail editor.
- **REQ-021-008**: Admin translation edits MUST save as draft and MUST NOT affect live clients until published.
- **REQ-021-009**: Admin MUST be able to import locale JSON files with validation preview and import history, choosing either Import as Draft or controlled Import and Publish Version.
- **REQ-021-010**: Admin MUST be able to export translation JSON files by locale, tenant/surface, group, and version, and MUST identify whether the export is draft or published.
- **REQ-021-011**: System MUST package published translation changes into immutable versioned bundles.
- **REQ-021-012**: System MUST allow Admin to roll back to a prior published translation bundle by creating a new rollback version.
- **REQ-021-013**: Published bundles MUST be the only translation source served to Patient, Provider, and Admin runtime clients.
- **REQ-021-013a**: Admin MUST be able to configure machine-translation provider credentials for draft generation, with notable provider options including Google Cloud Translation, DeepL, Microsoft Azure Translator, and Amazon Translate. (REQ-021-027)
- **REQ-021-013b**: Admin MUST be able to prefill all missing keys for a selected non-English language using machine translation, saving generated values as Review Needed drafts. (REQ-021-028)
- **REQ-021-013c**: Admin MUST be able to replace an entire selected non-English language with machine-generated draft values, excluding English/source values and requiring explicit confirmation. (REQ-021-029)
- **REQ-021-118**: The fallback notice on Patient App Language & Region Settings MUST be shown only when a fallback has occurred.
- **REQ-021-119**: When free-text translation is switched on, free text written by one user for another (messages, free-text fields in an inquiry, provider-authored package names and descriptions, support messages and notes, and reviews) MUST be machine-translated into the reader's own language using the active machine-translation provider. Uploaded documents MUST NOT be translated. The switch is one platform-wide setting controlled by Admin from the Free-text translation panel on Screen 10 and MUST be off by default.
- **REQ-021-120**: Admin MUST be able to configure a monthly budget for free-text translation in the Free-text translation panel on Screen 10 (no default figure); when the monthly limit is reached, free text MUST be shown untranslated.
- **REQ-021-121**: Only an admin holding the Manage Localization permission MUST be able to use the machine-translation route for translation drafts.
- **REQ-021-122**: The Manage Localization permission MUST cover editing non-English translation values, importing JSON as a draft, and generating machine-translation drafts. The Super Admin holds it and MAY grant it to another admin role in the FR-031 permission matrix. Editing the English source, changing the default locale, publishing, and rollback MUST stay Super Admin only.
- **REQ-021-123**: An import into the English source locale MUST be treated as an English source edit with the REQ-021-020 controls, and a new key created through import MUST carry an English value in the same file or the row is an error.
- **REQ-021-124**: Review Needed values MUST NOT block publish; the Screen 9 publish confirmation MUST show how many values remain flagged.
- **REQ-021-125**: Moving a locale from Preparation to Active MUST be Super Admin only and MUST require a published bundle for every surface (Patient App, Provider Dashboard, Admin Platform). The default locale MUST be Active.

### Data Requirements

- **REQ-021-014**: System MUST maintain a canonical translation registry with stable keys, source English values, tenant/surface metadata, group/namespace, locale values, lifecycle status, and history.
- **REQ-021-015**: System MUST validate placeholder variables, ICU syntax, duplicate keys, unknown keys, and required source values during edit/import/publish workflows.
- **REQ-021-016**: System MUST log missing translations and expose locale coverage metrics by tenant/surface, group, and locale.
- **REQ-021-017**: System MUST apply fallback per key when a selected locale value is missing.
- **REQ-021-018**: System MUST display dates/times in user timezone while storing canonical timestamps in UTC.
- **REQ-021-126**: Provider and admin screens MUST format dates and numbers by the selected locale. Provider screens MUST use the provider timezone set in FR-032 (a value from the FR-026 GMT list); admin screens MUST use the platform default timezone.
- **REQ-021-127**: Admin-authored library text (treatment type descriptions and technique specifications) MUST be registered as translation key groups on the Patient App and Provider Dashboard inventories. Provider-authored package names and descriptions are free text under REQ-021-119 and are not keys.
- **REQ-021-019**: System MUST display local currency with configured conversion, rounding, and locale-aware formatting.

### Security & Privacy Requirements

- **REQ-021-020**: English source value edits MUST require elevated authorization, reason capture, audit logging, and review-needed marking for dependent locale values once the edit passes validation, unless the Super Admin confirms the source change is non-semantic in the English edit dialog. A rejected edit marks nothing.
- **REQ-021-021**: System MUST audit locale changes, import confirmations, publish actions, rollback actions, protected source edits, and missing-translation events.
- **REQ-021-022**: Translation bundles and import/export files MUST NOT include patient medical data, private account data, or user-generated free text.
- **REQ-021-022a**: Machine translation requests for translation drafts MUST exclude patient medical data, private account data, user-generated free text, legal content, support messages, and uploaded documents unless another owning FR explicitly permits the content. Free-text translation for the reader follows REQ-021-119 instead. (REQ-021-030)
- **REQ-021-022b**: Machine-translation API credentials MUST be encrypted at rest, masked after save, access-controlled, and excluded from exports and audit payload details. (REQ-021-031)

### Integration Requirements

- **REQ-021-023**: System MUST provide published translation bundles consumable by Patient App, Provider Dashboard, and Admin Platform by locale and tenant/surface.
- **REQ-021-024**: System MUST provide locale/fallback behavior consumable by FR-030 notification template delivery.
- **REQ-021-025**: System MUST provide language/locale catalog data consumable by FR-032 provider spoken-language profile selection and FR-030 template-language selection, without conflating it with provider UI language preference. Interface-language selectors show Active locales only; the spoken-language and template-language lists show Active and Preparation locales.
- **REQ-021-026**: System MUST consume FR-029/S-02 currency conversion configuration for localized currency display and MUST NOT duplicate ownership of conversion rates, markup, rate locking, or payment fallback rules.

---

## Appendix: Change Log

| Date | Version | Changes | Author |
| --- | --- | --- | --- |
| 2026-11-24 | 1.8 | Logic review pass 1: one Manage Localization permission defined for everyday localization work with the four protected operations kept Super Admin only; import into the source locale treated as an English source edit; import with skipped error rows offers Import as Draft only; fallback chain and Screen 5 fallback control; Review Needed handling (accept as reviewed, marking after validation, publish not blocked); one machine-translation flow with connection check, preview and confirm, job statuses and provider enable/disable; Free-text translation panel on Screen 10; locale-aware date and number formatting rule; interface-language versus spoken-language lists; library text as key groups; notification wording removed from the registry surfaces; Preparation-to-Active rule. | Product Owner / Documentation |
| 2026-11-22 | 1.7 | Requirements graph programme baseline: PRD compressed to the checklist structure (each rule stated once, field rows tagged with graph field ids, dropped classes removed). No rule changes. Earlier history (v1.0 to v1.6) is in `archived/prd-baseline-2026-11-08/` and in git history. | Product Owner / Documentation |

---

## Appendix: Approvals

| Role | Name | Date | Signature/Approval |
| --- | --- | --- | --- |
| Product Owner | Joachim | 2026-05-25 | ✅ Approved |

---

**Template Version**: 2.0.0 (Constitution-Compliant)
**Constitution Reference**: Hairline Platform Constitution v1.0.0, Section III.B (Lines 799-883)
**Based on**: FR-011 Aftercare & Recovery Management PRD
**Last Updated**: 2026-11-24
