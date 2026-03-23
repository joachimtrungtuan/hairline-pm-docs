# Provider Dashboard Audit — Second-Pass Verification Corrections (2026-03-19)

## Summary

Deployed 5 parallel sub-agents to cross-check every `file:line` evidence reference in `audit_2026-03-18_provider.md` against the actual backend and frontend codebase. 6 verdict corrections applied; 2 module name errors in the summary table fixed; priority action items updated.

## File Updated

- `local-docs/testing-plans/2026-03-10/automated/provider-dashboard/audit_2026-03-18_provider.md`

## Verdict Corrections

| TC ID | Original Verdict | New Verdict | Root Cause of Error |
|-------|-----------------|-------------|---------------------|
| P-ONB-016 | CODE_EXISTS_CORRECT | **CODE_EXISTS_BUG** | `ProviderTeamController.php:1562` is `$member->delete()`, not a self-revoke guard. No self-revoke check exists anywhere in `destroy()`. |
| P-QOT-035 | NEEDS_DEEPER_REVIEW | **CODE_EXISTS_BUG** | Full read of `QuotesController::update()` (lines 4820–4936+) confirmed zero status guards — quotes of any status can be edited. |
| P-APT-015 | CODE_EXISTS_CORRECT | **NEEDS_DEEPER_REVIEW** | `QuotesController.php:208` is a patient-facing endpoint scoped by `patient_id`, not provider. Evidence pointed at the wrong endpoint; correct provider-scoped endpoint not yet confirmed. |
| P-TRT-021 | CODE_EXISTS_CORRECT | **CODE_EXISTS_PARTIAL** | `updateGrafts()` at line 5787 updates `estimated_grafts` only; no `actual_grafts` field exists in the Quote model. "Both values stored" was inaccurate. |
| P-TRT-028 | NEEDS_DEEPER_REVIEW | **CODE_EXISTS_PARTIAL** | `TreatmentPlanDailyEntryController::update()` confirmed: no date-based guard at all. Future days can be freely marked `in_progress`. |
| P-AFT-018 | NEEDS_DEEPER_REVIEW | **CODE_MISSING** | Full read of `getMilestoneDetails()` (lines 4979–5089): no pain-score threshold or auto-escalation trigger exists. `calculatePainLevel()` is a static display heuristic; `escalate()` is manual-only. |

## Updated Totals

| Verdict | Before | After |
|---------|--------|-------|
| CODE_MISSING | 1 | **2** |
| CODE_EXISTS_BUG | 15 | **17** |
| CODE_EXISTS_PARTIAL | 60 | **62** |
| CODE_EXISTS_CORRECT | 174 | **171** |
| NEEDS_DEEPER_REVIEW | 5 | **3** |
| **Total** | 255 | 255 |

## New Priority Action Items Added

- **P2 #4:** `QuotesController::update()` — no status guard allows edits to any status quote
- **P2 #5:** `ProviderTeamController::destroy()` — no self-revoke guard
- **P3 #16:** Auto-urgent pain escalation not implemented (P-AFT-018)
- **P3 #17:** Future treatment days can be marked In Progress (P-TRT-028)

## Summary Table Corrections (Non-Verdict)

- M08 label corrected: "Notifications (FR-020)" → "Treatment Completion (FR-010, FR-011)"
- M09 label corrected: "Billing & Payments (FR-007, FR-032)" → "Cross-Cutting Concerns (FR-020, FR-009)"

## M11 / M12 / M13 — Follow-Up Verification Pass (also 2026-03-19)

A follow-up verification pass was run for the three modules missed due to a rate limit. Additional corrections applied:

### Additional Verdict Changes

| TC ID | Original Verdict | New Verdict | Reason |
|-------|-----------------|-------------|--------|
| P-RAC-005 | CODE_EXISTS_CORRECT | **CODE_EXISTS_BUG** | Already-confirmed check at line 1039 is before `DB::beginTransaction()` at line 1046 — genuine TOCTOU race window outside transaction boundary |
| P-DAT-011 | CODE_EXISTS_PARTIAL | **CODE_EXISTS_CORRECT** | `createInstallmentPlan()` at line 312 applies last-installment residual adjustment — "no rounding compensation" claim was wrong |

### Additional Evidence Corrections (no verdict change)

- P-IDP-003: `custom_services` creation loop at lines 2184–2211 (not 1707 — was validation comment)
- P-RAC-003: `store()` at lines 97–124, `updateOrCreate()` at line 108 (not 135–141)
- P-DAT-001: `Quote::inquiry()` at lines 58–61 (not 59)
- P-DAT-002: `Booking::quote()` at lines 79–82 (not 211–214 — model is only 151 lines)
- P-DAT-009: `Payment.amount` at line 24 (not 23 — line 23 is `payment_number`)
- P-DAT-010: Deposit formula with `round()` is in `BookingService:122`, not `DepositRateService:106` (which is a snapshot helper without rounding)
- P-DAT-011: `createInstallmentPlan()` starts at line 287 (not 234 — lines 234–242 are the call site)

### Final Totals After All Corrections

| Verdict | Count |
|---------|-------|
| CODE_MISSING | 2 |
| CODE_EXISTS_BUG | **18** |
| CODE_EXISTS_PARTIAL | **61** |
| CODE_EXISTS_CORRECT | **172** |
| NEEDS_DEEPER_REVIEW | 3 |
| **Total** | **255** |

P3 defect #14 (installment sum not enforced) removed — P-DAT-011 corrected to CORRECT. New P2 defect #8 (P-RAC-005 TOCTOU on visit confirmation) added.
