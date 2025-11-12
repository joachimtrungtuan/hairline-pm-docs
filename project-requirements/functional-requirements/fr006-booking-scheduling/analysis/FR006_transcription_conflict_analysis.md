# FR-006 vs Transcriptions: Workflow & Rules Conflicts

Date: 2025-11-12
Scope: Booking & Scheduling (FR-006) compared to client transcriptions in `local-docs/project-requirements/transcriptions/`

## Summary

Overall alignment is high: provider pre-selects appointment during quote; patient accepts → proceeds to payment; booking is confirmed after payment; identity unmasking happens post-payment; interest-free split-pay completes ≥30 days pre-procedure. A few terminology and timing mismatches may create workflow ambiguity.

## Major Conflicts

1) Status terminology: “confirmed slot” vs “Confirmed booking”
   - FR-006 calls the pre-selected appointment “already confirmed” at quote acceptance, then sets booking to "Confirmed" after payment.
     - Evidence: `local-docs/project-requirements/functional-requirements/fr006-booking-scheduling/prd.md:81-88`
   - Transcriptions use “Scheduled” for the state after acceptance and reserve “Confirmed” for post-payment.
     - Evidence: `local-docs/project-requirements/transcriptions/HairlineApp-Part1.txt:187-203`
   - Impact: Ambiguous “confirmed” label for slot vs booking can confuse users and reporting. 

2) Visible stages in provider workflow
   - FR-006 provider data omits a distinct “Scheduled” status (lists Accepted / Confirmed / In Progress / Cancelled) while describing pre-scheduled slots.
     - Evidence: `local-docs/project-requirements/functional-requirements/fr006-booking-scheduling/prd.md:219-244`
   - Transcriptions explicitly describe tabs/sections: Quotes → Accepted → Scheduled → Confirmed, then suggest merging to 3 by auto-scheduling.
     - Evidence: `local-docs/project-requirements/transcriptions/Hairline-ProviderPlatformPart1.txt:239-257`
   - Impact: Mismatch in stage naming/visibility could misalign provider UI and analytics.

3) Payment needed to confirm: deposit vs “paid”
   - FR-006 confirms booking after deposit or initial installment; deposit default 20–30% (admin-configurable).
     - Evidence: `local-docs/project-requirements/functional-requirements/fr006-booking-scheduling/prd.md:83-88`, `:612-614`
   - Transcriptions state “confirmed is when the patient has paid” without specifying deposit vs full, while also defining split-pay that completes ≥30 days before.
     - Evidence: `local-docs/project-requirements/transcriptions/Hairline-ProviderPlatformPart1.txt:248-257`, `local-docs/project-requirements/transcriptions/Hairline-AdminPlatformPart2.txt:160-166`
   - Impact: If “paid” is interpreted as full payment, it conflicts with deposit/first-installment confirmation.

4) Hold windows: 48h vs 24h and offer validity vs payment-failure hold
   - FR-006 defines a 48-hour hold after deposit failure, but elsewhere says “hold 24 hours on failure” (internal inconsistency).
     - Evidence: `local-docs/project-requirements/functional-requirements/fr006-booking-scheduling/prd.md:110-115`, `:680-682`
   - Transcriptions specify quote/offer validity of “~48 hours” pre-acceptance.
     - Evidence: `local-docs/project-requirements/transcriptions/HairlineApp-Part1.txt:175-177`
   - Impact: Multiple windows with differing durations risk confusion for users and support.

## Clarifications (Aligned, but specify to avoid ambiguity)

- Provider pre-selects exact appointment time during quote; patient does not choose slot at booking.
  - Evidence: `local-docs/project-requirements/transcriptions/HairlineApp-Part1.txt:183-189`

- Identity unmasking after payment only (provider sees anonymized patient before that).
  - Evidence: `local-docs/project-requirements/transcriptions/Hairline-AdminPlatform-Part1.txt:36-48`

- Split-pay window offered dynamically and must complete ≥30 days pre-procedure (2–9 months typical).
  - Evidence: `local-docs/project-requirements/transcriptions/Hairline-AdminPlatformPart2.txt:160-166`

- Provider UI can be list/table based; no explicit need for a calendar view in transcriptions (FR-006 “no calendar” is acceptable if table supports the flow).
  - Evidence: `local-docs/project-requirements/functional-requirements/fr006-booking-scheduling/prd.md:221-244`

## Recommended Resolutions

1) Standardize status names and messaging
   - Use “Reserved” (or “Pre-scheduled”) for slot state post-acceptance. Reserve “Confirmed” strictly for post-payment booking.
   - Option A: Keep four internal states (Accepted → Reserved → Confirmed → In Progress) but display three in provider UI by merging Accepted+Reserved into “Accepted (Reserved)”.
   - Option B: Keep three states externally (Accepted → Confirmed → In Progress) and treat slot reservation as an internal flag.

2) Clarify confirmation predicate in UI copy
   - Confirm booking after deposit or first installment, not necessarily full amount. Update user-facing copy from “paid” to “payment made (deposit or first installment)”.

3) Unify hold durations and name the windows
   - Adopt 48 hours as default for both: (a) quote/offer validity pre-acceptance and (b) post-payment-failure reservation hold; make both admin-configurable. Remove the 24-hour mention in FR-006.

4) Document currency and FX behavior as dependencies
   - Reference FR-029: Payment System Configuration for region-based currency, Stripe mappings, and FX margin/lock rules to avoid ambiguity in FR-006.

## Next Actions

- Update FR-006 language: replace “appointment slot already confirmed” with “slot reserved/pre-scheduled”.
- Add an explicit state diagram callout matching chosen Option A or B above.
- Replace 24-hour reference with 48 hours, mark both windows configurable.
- Adjust confirmation copy to “deposit/first installment confirms booking; full balance due per schedule”.

