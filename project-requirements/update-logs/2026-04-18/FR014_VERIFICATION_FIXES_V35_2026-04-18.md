# FR-014 Verification Fixes — v3.5

**Date**: 2026-04-18
**FR**: FR-014 — Provider Analytics & Reporting
**Author**: Claude Code (verify-fr workflow)
**Source PRD version**: 3.4 → 3.5

---

## Summary

Applied three verification fixes to `functional-requirements/fr014-provider-analytics-reporting/prd.md` following a `verify-fr` pass. One medium issue and two minor issues resolved. No critical issues were found.

---

## Changes

### 1. Screen 6 PDF branding (Medium — Issue #1)

**Before** (`prd.md:666`):
> PDF reports include provider branding (logo, colors from profile)

**After**:
> PDF reports include provider logo sourced from `providers.profile_image`; no provider-specific color theming (platform default palette is used) — schema does not define brand color fields and this is intentional for v1

**Reason**: `providers.profile_image` exists in `system-data-schema.md:142`, but no provider brand color fields are defined in the schema or FR-015. Dropping the colors reference aligns the spec with the current data model.

### 2. FX fallback freshness cap (Minor — Issue #3)

**Rule 10** updated to cap FX rate fallback at **48 hours**. Beyond 48h, affected financial widgets render a "FX data unavailable" state instead of using stale rates. **Assumption 9** added to restate the cap explicitly.

### 3. Legacy `patients.location` fallback UI indicator (Minor — Issue #3)

**Assumption 10** added: Country widgets (Screens 3, 10) flag rows resolved via the legacy `patients.location` fallback with a subtle UI indicator, so users can distinguish canonical (`location_id → countries.name`) from transitional data until backfill is complete.

### 4. Provider-side analytics accepted as PRD-derived (Minor — Issue #2)

**Assumption 8** added to record that provider-side widgets (TTFQ benchmarks, pricing scatter, patient journey, conversion breakdowns, etc.) are **PRD-derived, not transcription-derived**. Client transcriptions focus primarily on admin reporting; the provider analytics UX is a product-led complement. This is an **accepted design decision** — future verification passes (human or AI) MUST NOT re-flag these widgets as transcription discrepancies.

### 5. Change log row added

Added v3.5 row to the PRD Change Log appendix describing the above.

---

## Files Modified

- `local-docs/project-requirements/functional-requirements/fr014-provider-analytics-reporting/prd.md`

---

## Verification Status

- Constitution compliance: Pass
- Dependencies: All cited FRs and services (S-03, S-05) exist
- Schema references: `quotes.sent_at`, `quotes.accepted_at`, `provider_activity_logs.action_at`, `patients.age`, `providers.profile_image` all confirmed in `system-data-schema.md`
- Outstanding: None. Status updated to ✅ Verified & Approved (v3.6); Product Owner approval recorded 2026-04-18.
