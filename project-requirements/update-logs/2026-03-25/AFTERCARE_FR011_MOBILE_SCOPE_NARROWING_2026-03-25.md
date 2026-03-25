# Aftercare FR-011 Mobile Scope Narrowing

**Date**: 2026-03-25
**Type**: Verification report scope update
**Scope**: Narrow the existing Aftercare relationship report to `FR-011` patient mobile screens only
**Source Spec**: `local-docs/project-requirements/functional-requirements/fr011-aftercare-recovery-management/prd.md`
**Platform**: Patient Mobile App

## Summary

Updated the existing report at `local-docs/reports/2026-03-24/design-layout-verification-fr011-patient-mobile.md` so it now covers only the `FR-011` patient-mobile screen set and excludes the previous `FR-010` / `P05.*` relationship audit material.

## Changes Applied

- Report title updated to `FR-011 Patient Mobile`
- Report date updated to `2026-03-25`
- Scope reduced to `FR011-W2`, `FR011-W2b`, and `FR011-W3` only
- Report file renamed to `design-layout-verification-fr011-patient-mobile.md` so the path matches the narrowed scope
- Layout inventory reduced to `layout-temp/aftercare/` and related FR-011 patient-mobile mappings only
- Out-of-scope `P05.*`, `layout-temp/in progress/`, and `layout-temp/reviews/` sections removed from the verification body
- Action items rewritten to reflect only FR-011 mobile gaps

## Verification Outcome

- `FR011-W2 🔴 BLOCKED`
- `FR011-W2b 🔴 BLOCKED`
- `FR011-W3 🔴 BLOCKED`
- In-scope screen mapping remains `9 / 9`, but checkout, questionnaire, and educational-resource screens still fail field-level verification

## Impact

- The updated report is now a clean FR-backed artifact for `FR-011` patient mobile review only
- Any future questions about `P05.*` mobile complement coverage should use the broader March 24 relationship audit or the dedicated `P05` reports, not this narrowed FR-011 report

## Minor Follow-Up

- Rechecked the report under a shared tabbed-interface interpretation: fields already satisfied by the common Aftercare shell are no longer expected to repeat on every tab; this downgraded `FR011-W3 Screen 5 Educational Resources` from `🔴 FAIL` to `🟡 PARTIAL` and reduced the corresponding action item from critical to important
- Rechecked `FR011 Screen 7` against the already-verified shared payment-method flow in `local-docs/reports/2026-03-24/design-layout-verification-missing-mobile-flows-design-complement-p03.1.md`; card-entry and billing-address fields are satisfied through `P03.1-S2 Add/Edit Payment Method`, so they are no longer treated as missing from the FR-011 checkout layouts themselves
- Rechecked `FR011 Screen 6` as well: unlike Screen 7, its `Payment Method`, `Selected Payment Method`, and `Total Amount` requirements remain valid on Screen 6 itself because FR-011 places the pricing choice and total-before-payment step before the checkout handoff; the Screen 6 verdicts therefore remain unchanged
- Further clarified the Screen 6 finding after rechecking the checkout images directly: the pricing choice and total do exist in the design, but they are currently shown in the Screen 7 checkout layouts rather than on Screen 6, so the report now describes this as a Screen 6 vs Screen 7 boundary mismatch instead of saying those fields are absent from the design flow overall
- Corrected the `Screen 6` field-status markers for those shifted fields from plain missing (`❌`) to mismatch (`❌⚠️`) so the table now reflects that the pricing choice and total are present in the design, but on the adjacent checkout screen rather than on Screen 6 itself
