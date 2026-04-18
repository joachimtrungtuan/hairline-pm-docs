# FR-014 Backend Alignment

**Date**: 2026-04-18  
**Scope**: FR-014 Provider Analytics & Reporting, `system-prd.md`

## Summary

Applied the user-selected follow-up resolutions from the FR-014 verification pass and cross-checked Issue 1 against the Laravel backend.

## Changes Applied

1. Normalized patient-country provenance in FR-014 to the backend-supported source:
   - Canonical source is `patients.location_id -> countries.id/name`
   - Legacy `patients.location` is retained only as a temporary fallback for unmigrated rows
   - Removed the unsupported IP-geolocation fallback assumption from FR-014

2. Aligned the FR-014 system PRD summary with the approved SLA decision:
   - Changed admin-configurable SLA from per-provider to a single platform-wide target

3. Closed the export dependency gap in FR-014:
   - Added `S-03: Notification Service` for scheduled export email delivery / secure-link notifications
   - Added `S-05: Media Storage Service` for 7-day artifact retention and re-download access

## Backend Evidence Used

- `main/hairline-backend/app/Models/Patient.php`
  - `location_id` is the patient foreign key
  - `country()` maps `location_id` to `Country`

- `main/hairline-backend/database/migrations/2025_12_02_131928_change_location_id_to_reference_countries_in_patients_table.php`
  - Migrates patient `location_id` from `locations` to `countries`

- `main/hairline-backend/app/Http/Controllers/Authentication/AuthController.php`
  - Rehydrates display `location` from `country->name`

- `main/hairline-backend/app/Http/Controllers/Quotes/QuotesController.php`
  - Uses `COALESCE(countries.name, patients.location)` showing canonical country + legacy fallback behavior

- `main/hairline-backend/app/Http/Controllers/Analytics/AnalyticsController.php`
  - Still aggregates on legacy `patients.location`, confirming transition cleanup is incomplete and should be documented explicitly

## Outcome

FR-014 is now aligned with the selected resolutions and better matches the current backend implementation path while preserving a documented transition state for legacy patient location data.
