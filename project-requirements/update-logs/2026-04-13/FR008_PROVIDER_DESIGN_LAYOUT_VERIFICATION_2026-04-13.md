# FR-008 Provider Design Layout Verification — 2026-04-13

**Date**: 2026-04-13
**Type**: Design Layout Verification
**Scope**: FR-008 Travel & Logistics Coordination — full provider scope (`Main Flow 1` + `Main Flow 2`)
**Report**: `local-docs/reports/2026-04-13/design-layout-verification-fr008.md`

---

## Summary

Verified the full FR-008 provider-platform scope against the current `layout-temp/` assets, covering:

- `Screen 6` — Travel Section / Booking-Quote Detail (Path A + Path B variants)
- `Screen 7` — Passport View (Provider)
- `Screen 8` — Flight Information / Provider Entry (Path A)
- `Screen 9` — Hotel Information / Provider Entry (Path A)
- `Screen 10` — Travel Details / Booking-Quote Detail (Provider, Path B)

This pass supersedes the narrower `2026-04-02` provider review by validating both provider flows end-to-end instead of only reviewing a selected screen subset.

## Overall Verdict

**Mixed result**:

- `Main Flow 1: Provider-Included Travel` → **🟡 PARTIAL**
- `Main Flow 2: Patient Self-Booked Travel` → **🔴 BLOCKED**

Screen-level results:

| Screen | Description | Status | Field Coverage |
|--------|-------------|--------|----------------|
| S6 (Path A) | Travel Section — Booking/Quote Detail | 🟡 PARTIAL | 83% (5/6) |
| S7 | Passport View — Provider | 🟢 COMPLETE | 100% (9/9) |
| S8 | Flight Information — Provider Entry | 🟢 GOOD | 100% (13/13) |
| S9 | Hotel Information — Provider Entry | 🟢 COMPLETE | 100% (13/13) |
| S6 (Path B) | Travel Section — Booking/Quote Detail | 🟡 PARTIAL | 83% (5/6) |
| S10 | Travel Details — Provider / Path B | 🔴 FAIL | 40% (2/5 grouped checks) |

## Scope

- Requirement source: `local-docs/project-requirements/functional-requirements/fr008-travel-booking-integration/prd.md`
- Layout source: `layout-temp/`
- Platform: Provider Web
- Unmapped context files cataloged but excluded from verdicts:
  - `layout-temp/Confirmed.jpg`
  - `layout-temp/Confirmed Filter.jpg`
  - `layout-temp/Fulltable overview.jpg`

## Key Findings

1. **Provider-included travel is largely designed, but the booking-detail review states still drift off-spec.**
   - The Path A tracker correctly shows travel path and status badges.
   - The passport review content is present and usable.
   - The main remaining gap is action/state integrity on Screen 6: the design merges Screen 6 and Screen 7 inline, and later submitted states expose `Edit ... details` even though submitted provider records should be locked.

2. **Provider entry forms are implementation-ready with one targeted cleanup.**
   - Screen 8 includes the full outbound/return flight entry structure and a clear `Save flight details` CTA.
   - Screen 9 includes the full hotel-entry structure and a clear `Save hotel details` CTA.
   - The only form-level spec drift is an extra `Total Price` field in one Screen 8 typing variant, even though FR-008 explicitly excludes price capture from this screen.

3. **Patient self-booked provider review is still blocked by missing/incorrect submitted-state coverage.**
   - The Path B awaiting tracker exists and correctly hides passport status.
   - The required `View Travel Details` action is missing from the Path B Screen 6 tracker.
   - `Patient Self-Booked Travel/Flight details.jpg` does not provide an outbound-flight detail view; it resolves to the same hotel-detail presentation as the hotel asset.
   - The hotel-detail state itself has field/value binding errors (`Check-in Time` shows a date; `Check-Out date` shows a time).

## Follow-Up Actions

1. Add the missing `View Travel Details` action to the Path B tracker on Screen 6.
2. Design distinct submitted-state views for Path B hotel, outbound flight, and return flight.
3. Remove or redesign the `Edit ... details` behavior from submitted Path A review states so it matches the record-locking rule.
4. Remove `Total Price` from the provider flight-entry form.
5. Decide whether the merged Screen 6 + Screen 7 passport pattern is intentional; if yes, update the PRD explicitly instead of leaving the design/spec mismatch implicit.

## Traceability

- Full report: `local-docs/reports/2026-04-13/design-layout-verification-fr008.md`
- Prior targeted provider review: `local-docs/project-requirements/update-logs/2026-04-02/FR008_PROVIDER_DESIGN_LAYOUT_VERIFICATION_2026-04-02.md`
- Requirement source: `local-docs/project-requirements/functional-requirements/fr008-travel-booking-integration/prd.md`
