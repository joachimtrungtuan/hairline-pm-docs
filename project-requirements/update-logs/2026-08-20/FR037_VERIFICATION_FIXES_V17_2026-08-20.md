# FR-037 Verification Fixes (v1.6 → v1.7)

**Date**: 2026-08-20
**Type**: FR revision + cross-document alignment
**Documents changed**: `functional-requirements/fr037-monitor-hair-loss/prd.md`, `system-prd.md`

---

## Context

`/verify-fr FR-037` raised 2 critical, 4 medium, and 2 minor findings. Product owner confirmed FR-037 originates from an extra requirement, not from the client transcriptions, so transcription-traceability findings were void. Remaining accepted findings are fixed below.

## Changes

### 1. Provider anonymization (critical)

Screen 9 previously hid patient identity "before payment confirmation", but FR-037 contains no payment event, leaving the de-anonymization trigger undefined.

- Screen 9 Case Header validation now reads: anonymized patient identifier only, for the entire case lifetime.
- Added Screen 9 business rule stating FR-037 has no payment and any de-anonymization occurs only in the FR-003/FR-004 flow produced by conversion.
- Added a Data & Privacy rule and `REQ-037-030`.

### 2. Cadence naming (medium)

"Twice monthly" implied 24 windows per year while the rule implements a 14-day minimum interval (~26 per year). Renamed to **bi-weekly** throughout the PRD (Module Scope, Screen 13, Rule 5, Admin Editability, `REQ-037-008`), matching the meeting-confirmed "once a week or once every two weeks" model.

### 3. Conversion Step B handoff (medium)

The Step B field table listed "Inquiry-Only Fields" as a required Step B field while its business rule assigned those fields to FR-003 screens. Relabelled to **Inquiry-Only Handoff Target** (type `reference`), explicitly not collected or validated on Step B. Step B remains the gateway into the FR-003 inquiry screens.

### 4. Multiple entries on one date (minor)

Severity derivation was undefined when a date holds several entries. Added Rule 9, a Screen 3 business rule, `REQ-037-031`, and a `MonitoringEntry` submission-timestamp attribute: the latest-timestamped entry on a date is authoritative for that date's trend, latest-severity, and PDF summary values; superseded entries remain stored and auditable.

### 5. system-prd.md synchronization (medium)

FR-037 capabilities that existed only in the detailed PRD were backported to `system-prd.md` §FR-037:

- Modules extended with S-03: Notification Service and S-05: Media Storage Service.
- Global cadence captured at case creation; renamed weekly / bi-weekly.
- Advice-window open-until-submitted behavior with supersession-only expiry.
- Advice as a separate provider-authored calendar record with immutable edit history.
- Expiring, revocable, audited pre-assignment case-preview links with no embedded chat.
- Provider-facing anonymized patient identifier for the entire case lifetime.

## Not changed

- **Patient scan reminders**: out of scope by product-owner decision; the self-service vs aftercare boundary stands.
- **Retention**: PRD keeps the project-standard 7 years. Note that `constitution.md:645` specifies 10-year retention for audit trails specifically; unchanged pending a governance decision.

## Result

FR-037 PRD version 1.7. No orphaned screen fields; no dependency business-rule or data-field conflicts found against FR-002, FR-003, FR-004, FR-020, FR-025, FR-026, FR-028.
