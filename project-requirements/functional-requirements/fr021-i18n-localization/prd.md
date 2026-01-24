# FR-021 - Multi‑Language & Localization

**Module**: A-09: System Settings & Configuration | S-02: Payment Processing Service
**Feature Branch**: `fr021-i18n-localization`
**Created**: 2025-11-11
**Status**: Draft
**Source**: FR-021 from local-docs/project-requirements/system-prd.md; Transcriptions (platform references)

---

## Executive Summary

Enable multi‑language and localization across Hairline products: users can choose their preferred language, UI and notifications are translated, dates/times reflect user timezone, and prices display in local currency with conversion. Initial languages: English and Turkish; RTL (e.g., Arabic) is planned. Centralized configuration controls supported locales, defaults, and currency settings.

---

## Module Scope

### Multi-Tenant Architecture

- Patient Platform (P): Language selection, localized UI and notifications, timezone‑aware dates/times, local currency display.
- Provider Platform (PR): Language selection, localized UI and ops emails, timezone and currency display aligned to profile settings.
- Admin Platform (A-09): Manage supported locales, default/fallback order, translation assets, and currency display rules; view coverage reports.
- Shared Services (S-02): Currency conversion source and formatting; locale formatting utilities shared across tenants.

### Scope Boundaries

In Scope:

- Language selection per user; default/fallback behavior when content not translated.
- Translation of UI strings, system emails, and push notifications for initial locales.
- Timezone‑aware date/time formatting based on user profile/device.
- Currency display using user’s locale with conversion and rounding policies.

Out of Scope (V1):

- Content translation for user‑generated text (reviews/messages) beyond UI chrome.
- RTL layout delivery (tracked; planned next phase preparedness noted below).

### Entry Points

- Users set language in Account/Settings; Admin sets platform default and supported list.
- Currency display derives from user locale and/or selected country in flows.

---

## Business Workflows

### Main Flow: User Selects Language

Actors: Patient/Provider, System
Trigger: User changes language in Settings
Outcome: UI and notifications switch to selected language; preference is remembered

Steps:

1. User opens Settings → Language and chooses a supported locale.
2. System persists preference and reloads UI resources.
3. Emails/push notifications for that user use the chosen locale.
4. If a string is missing, fallback order is applied (locale → default).

### Alternative Flows

- A1: Missing Translation
  - Trigger: A string has no translation in target locale.
  - Outcome: System falls back to default language string and logs for coverage.

- B1: Unsupported Locale
  - Trigger: User/device requests an unsupported locale.
  - Outcome: System selects nearest supported (language match) or platform default.

### Currency and Timezone Display

Actors: User, System, Currency Source
Trigger: Price or scheduled time is shown
Outcome: Values reflect user locale and timezone

Steps:

1. Determine user locale/timezone (profile or device‑reported with consent).
2. Format numbers, dates/times using locale rules; convert currency as configured.
3. Display currency code/symbol per locale; show conversion rate context where appropriate.

---

## Screen Specifications

### Screen 1: Patient/Provider – Language & Region Settings

Purpose: Let users select language and review region formats.

Data Fields:

| Field Name       | Type   | Required | Description                         | Validation Rules                  |
|------------------|--------|----------|-------------------------------------|-----------------------------------|
| Language         | select | Yes      | Preferred language (EN, TR initial) | Must be in supported locales list |
| Region/Locale    | select | No       | Regional formatting (dates/currency)| From supported locale variants    |
| Timezone         | select | No       | Preferred timezone                  | Valid IANA timezone               |

Business Rules:

- Changes apply immediately; persisted to user profile.
- If locale not chosen, derive from language and country context.

Notes:

- Explain that some content may appear in default language if not yet translated.

---

### Screen 2: Admin – Localization Settings

Purpose: Configure platform locales and currency settings.

Data Fields:

| Field Name          | Type  | Required | Description                               | Validation Rules                     |
|---------------------|-------|----------|-------------------------------------------|--------------------------------------|
| Supported locales   | list  | Yes      | Add/remove locales (codes + names)        | ISO language/region codes            |
| Default locale      | select| Yes      | Fallback default                          | Must be in supported list            |
| Fallback order      | list  | No       | Ordered list of fallback locales          | No cycles/duplicates                 |
| Currency settings   | form  | Yes      | Source, refresh cadence, rounding policy  | Safe bounds; audit changes           |
| Coverage dashboard  | panel | No       | % of strings translated per locale        | N/A                                  |

Business Rules:

- Changes are audited; effective immediately upon save.
- Disabling a locale removes it from user selection but preserves data.

---

## Success Criteria

- SC-001: 99% of UI strings load in the selected language for supported locales (coverage measured per release).
- SC-002: 100% of system emails/push templates render in selected language or fallback when missing.
- SC-003: Dates/times reflect user timezone across the app with no incorrect cross‑day conversions in 99.9% of cases.
- SC-004: Currency displays in user locale with accurate conversion (within configured rate source tolerance) for 99% of views.
- SC-005: Switching language completes in ≤ 2 seconds for 95th percentile.

---

## Business Rules

- All UI strings externalized; no hard‑coded user‑facing text.
- Fallback logic applies per string; missing entries flagged for localization.
- Timezone and currency formatting use locale‑aware libraries consistently.
- RTL readiness: components follow mirroring rules; full RTL rollout tracked as a follow‑up.

### Admin Editability

Editable by Admin:

- Supported locales, default locale, fallback order.
- Currency configuration (source, refresh cadence, rounding/markup display policy).

Fixed in Codebase (Not Editable):

- Locale/number/date formatting standards; list of mandatory template keys.

Configurable with Restrictions:

- Maximum number of concurrently supported locales (for performance/QA capacity).

---

## Dependencies

- S-02: Payment Processing Service for currency conversion source and rounding.
- S-03: Notification Service for localized templates.
- P/PR apps for string externalization and preference surfaces.

---

## Assumptions

- Initial locales: English (en), Turkish (tr); Arabic (ar) next for RTL.
- Currency conversion updated at least daily; displayed values rounded per policy.
- Users can override device language with explicit profile preference.

---

## Implementation Notes

- Use structured translation resources (keys with ICU message format).
- Maintain per‑locale template sets for emails/push; validate required keys.
- Provide linting/checks for untranslated or orphan keys in CI.
- Ensure timezone handling respects server/client boundaries (store in UTC, display in local).

---

## User Scenarios & Testing

### User Story 1 – User switches to Turkish (P1)

Why: Provide localized experience.

Independent Test: Change language to Turkish; UI strings and emails render in Turkish; fallback used for missing.

Acceptance Scenarios:

1. Given supported Turkish, when user selects tr, then UI and emails render in tr or fallback.
2. Given tr selected, when a string is missing, then default language value is shown and logged.

### User Story 2 – Admin adds new locale (P1)

Why: Expand market support.

Independent Test: Add locale in Admin; users can select it and UI loads for available strings.

Acceptance Scenarios:

1. Given a new supported locale, when saved, then it appears in user settings.
2. Given templates uploaded, when emails send, then they render in the new locale.

### User Story 3 – Local currency and timezone (P2)

Why: Improve comprehension and trust.

Independent Test: Prices and times display in user locale and timezone.

Acceptance Scenarios:

1. Given user locale, when price is shown, then symbol/format match locale and conversion is applied.
2. Given user timezone, when appointment is displayed, then local time is shown correctly.

---

## Functional Requirements Summary

- **REQ-021-001**: System MUST support multiple languages (initial EN, TR; RTL planned).
- **REQ-021-002**: Users MUST be able to select preferred language; preference persists across sessions/devices.
- **REQ-021-003**: System MUST translate UI strings, emails, and push notifications for supported locales with fallback.
- **REQ-021-004**: System MUST display dates/times in user timezone.
- **REQ-021-005**: System MUST display local currency with conversion and correct formatting.
- **REQ-021-006**: Admins MUST be able to manage supported locales, defaults, and currency settings.
- **REQ-021-007**: System MUST log missing translations and locale coverage metrics.

---

## Key Entities

- Locale: code, name, enabled, fallback order.
- TranslationResource: key, locale, value, updatedAt, coverage status.
- CurrencyConfig: source, refresh cadence, rounding/markup policy, lastUpdated.

---

## Appendix: Change Log

| Date       | Version | Changes                                     | Author |
|------------|---------|---------------------------------------------|--------|
| 2025-11-11 | 1.0     | Initial PRD creation                        | AI     |

---

## Appendix: Approvals

| Role           | Name | Date | Signature/Approval |
|----------------|------|------|--------------------|
| Product Owner  |      |      |                    |
| Technical Lead |      |      |                    |
| Stakeholder    |      |      |                    |

---

**Template Version**: 2.0.0 (Constitution-Compliant)
**Constitution Reference**: Hairline Platform Constitution v1.0.0, Section III.B (Lines 799-883)
**Last Updated**: 2025-11-11
