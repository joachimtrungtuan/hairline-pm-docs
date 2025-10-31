# FR-004 PRD Updates - October 31, 2025

Status: ✅ Completed

Scope: Update Quote Submission & Management PRD to align with design, policy, and system PRD.

## Changes

- Expiry Policy: Admin-controlled expiry window with default 48 hours; providers see computed deadline only.
- Provider Withdrawal After Acceptance: Added workflow for exceptional provider withdrawal, with admin resolution (reroute/reschedule/refund) and full audit. Noted potential split into a separate FR if policies expand.
- Cascading Scenarios:
  - When any provider’s quote is accepted, all other quotes for the same inquiry are auto-marked “cancelled (other accepted)” and providers are notified.
  - Drafting providers are immediately notified upon another quote acceptance; drafting quote locks with banner and case status updates.
- Quote Creation Screen: Rewrote to match implemented field order and content, including detailed package customization, graft estimation, per-date pricing for selected patient date ranges, clinician, plan, notes, read-only summary, and expiry display.
- Treatment vs Package: Clarified treatment (admin-controlled, compulsory) vs package (provider-bounded, optional); package customization is per-quote.
- Quote List: Unified (no tabs) with specified columns (anonymized ID, censored name, age, concern, treatment & package, date ranges quoted, multi-price, location, medical alerts, quoted date, action) and extended filters.
- Data Inheritance & Privacy: Quote data appends to inquiry data (no overwrites); downstream stages inherit upstream data; patient remains censored until payment.
- Admin Inline Edit: Added inline edit capability (price per date, inclusions, notes, clinician) with audit reason and re-notifications on impactful changes.
- Screen Numbering: Added coded screen numbers for all screens (Provider S1–S3, Patient S4, Admin S5–S6).

## Impact

- Aligns PRD with implemented UI flow and design components.
- Reduces ambiguity around expiry and cross-quote state handling.
- Reinforces compliance: audit logging, soft deletes, data retention, anonymization.

## Files Updated

- `local-docs/project-requirements/functional-requirements/fr004-quote-submission/prd.md`

## Follow-ups

- Consider extracting “Provider Withdrawal After Acceptance” into a standalone FR if refund/penalty/assignment policies grow.
