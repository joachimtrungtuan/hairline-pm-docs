# Update Log — 2026-04-23

**Type**: New Artifact — Mobile Bug Report Skeleton  
**Date**: 2026-04-23

## Summary

Created `local-docs/reports/2026-04-23/mobile-bug-report-hl61.md`: a concise mobile bug report table skeleton starting from `HL61`.

## What Was Created

- **File**: `local-docs/reports/2026-04-23/mobile-bug-report-hl61.md`
- One-row starter template for `HL61`
- Required bug fields included: Pre-condition, Test steps, Test data, Expected result, Actual result, Screenshot
- Spreadsheet-style columns preserved: Date, Description & Screenshot/video, Bug Status, Reported By, Issue Type, Platform, Device & OS version, Comments

## Follow-up Updates

- Filled `HL61` with the Android bug report for non-cancelled inquiries incorrectly appearing in the Cancelled tab due to likely filtering on `cancelled_quotes > 0` instead of inquiry-level cancellation status.
- Added `HL62` for the static/fake quote expiry countdown on the Offers listing screen.
- Added `HL63` for the offer-list to quote-detail price/treatment-time mismatch when `treatment_date_id` is not passed into quote detail.
- Expanded `HL63` with live backend cross-check details: inquiry detail reports `total_offers=4`, offers list returns 4 treatment-date rows, the app displays 2 provider cards, and quote detail totals are `144` higher than list `total_price` because detail includes the `120` custom service before commission.
- Replaced local screenshot filenames for `HL61`, `HL62`, and `HL63` with clickable LetWeb Markdown links.
- Added `HL64` for the Offers filter not applying the selected max-price criteria; the app still displays a `$10,900` offer after applying `Max Price ($)=5,000`.
- Normalized `HL61`-`HL63` screenshot links so the Markdown link text exactly matches the linked LetWeb URL.
- Replaced `HL64` local screenshot filenames with clickable LetWeb links whose labels match the URLs.
- Clarified `HL63` expected behavior using the supplied design: provider quote cards/details should show multiple treatment-date price options instead of exposing only one visible option per provider.
- Added `HL65` for the Compare Offers table not exposing the full comparison information shown in the supplied design.
- Added `HL66` for quote acceptance missing the treatment-date selection bottom sheet shown in the supplied design.
- Added `HL67` for provider profile languages rendering raw JSON/object data instead of clean language names.
- Added `HL68` for the Travel Itinerary screen not matching backend itinerary data: return flight is submitted in the API but shown as not submitted in the app, and submitted-time/procedure-date field bindings appear inconsistent.
- Added `HL69` for Treatment process status labels rendering raw backend enum values (`finished`, `in_progress`, `not_started`) instead of user-friendly labels.
- Added `HL70` for package-backed quote inclusions rendering incorrectly: `included_services` is displayed as raw serialized objects, while `travel_package_inclusions` includes a row not returned by the backend payload.
- Added the eight supplied LetWeb screenshot links to the `HL70` bug report entry.
