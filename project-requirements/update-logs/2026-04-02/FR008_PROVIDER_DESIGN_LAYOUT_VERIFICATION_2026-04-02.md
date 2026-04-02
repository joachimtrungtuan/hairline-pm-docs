# FR-008 Provider Design Layout Verification — 2026-04-02

## Summary

Verified `FR-008 - Travel & Logistics Coordination` provider-side screens `6` through `10` against the current `layout-temp/` assets. Full field-by-field analysis recorded in:

- `local-docs/reports/2026-04-02/design-layout-verification-fr008-screen-6-10.md`

Screen-level results:

| Screen | Description | Status | Field Coverage |
|--------|-------------|--------|----------------|
| S6 | Travel Section — Booking/Quote Detail (Provider) | 🔴 FAIL | 0% (0/6) |
| S7 | Passport View — Provider | 🟢 GOOD | 100% (9/9) |
| S8 | Flight Information — Provider Entry (Path A) | 🟢 GOOD | 100% (13/13) |
| S9 | Hotel Information — Provider Entry (Path A) | 🟢 GOOD | 100% (13/13) |
| S10 | Travel Details — Booking/Quote Detail (Provider, Path B) | 🔴 FAIL | 45% (13/29 fields evidenced; submitted state still off-spec) |

## Scope

- Requirement source: `local-docs/project-requirements/functional-requirements/fr008-travel-booking-integration/prd.md`
- Verified screens: `Screen 6`, `Screen 7`, `Screen 8`, `Screen 9`, `Screen 10`
- Layout source: `layout-temp/` — 10 files total
- Platform: Provider Web

## Key Findings

1. **Screen 6 is missing the core travel status model.**
   - No `Travel Path`, `Passport Status`, `Outbound Flight Status`, `Return Flight Status`, or `Hotel Status` badges are visible in the reviewed Screen 6 state.
   - The supplied Path A states use off-spec actions (`Book hotel`, `Book flight`, later `Edit ... details`) instead of the required Screen 6 action model (`View Passport`, `Enter Flight`, `Enter Hotel`).
   - The travel area jumps between an empty passport state and composite review panels without ever surfacing the required status-first orchestration step.

2. **Screen 7 is usable, but it is embedded rather than clearly separated from the booking detail context.**
   - All 9 required passport fields are present, including full-number visibility and the passport image.
   - The layout remains inline inside the booking page and introduces shortcut buttons (`Book hotel`, `Book flight`) that behave more like Screen 6 navigation than pure Screen 7 read-only content.

3. **Screens 8 and 9 are largely correct provider-entry forms, with targeted follow-up only.**
   - Screen 8 includes all required flight-entry fields plus the outbound/return tabs required by the flow.
   - The main Screen 8 defect is an extra `Total Price` field in one variant, even though the PRD explicitly excludes price capture from this form.
   - Screen 9 includes all required and optional hotel-entry fields. The main follow-up is helper-copy clarity on the check-out/phone rows.

4. **Screen 10 is still a hard fail, but the evidence set is now clearer and more specific.**
   - `Awaiting patient’s hotel & flight details.jpg` is the correct Path B awaiting-state view, and `Hotel details.jpg` is a Path B hotel submitted-detail variant because it carries the patient-owned banner.
   - The hotel submitted-detail state is still non-compliant: it exposes `Edit Hotel details` even though Path B must be read-only, and the hotel labels are populated with flight-derived values such as `Turkish Airlines`, `TK142`, airport names, baggage, price, and meal-request text.
   - Outbound-flight and return-flight submitted states are still not evidenced, and `Submitted By` / `Status` metadata is missing even in the hotel submitted state.

## Follow-Up Actions

1. Redesign `Screen 6` with a spec-compliant travel tracker: Travel Path badge, passport/flight/hotel status badges, and the required action buttons.
2. Keep the existing Screen 7 content but either isolate it more clearly as a dedicated read-only passport view or connect it back to Screen 6 with the specified `View Passport` action.
3. Remove `Total Price` from `Screen 8`; keep price capture at the quote/package layer only.
4. Rebuild Path B submitted-detail review as read-only, rebind the hotel labels to the hotel schema, add the missing `Submitted By` / `Status` metadata, and supply compliant outbound-flight and return-flight submitted or pending states.

## Traceability

- Report artifact: `local-docs/reports/2026-04-02/design-layout-verification-fr008-screen-6-10.md`
- Requirement source: `local-docs/project-requirements/functional-requirements/fr008-travel-booking-integration/prd.md`
