# FR-017 Post-Verification Fixes

**Date**: 2026-04-01
**Type**: Major Update
**Affected Documents**:
- `local-docs/project-requirements/functional-requirements/fr017-admin-billing-finance/prd.md` (v1.1 → v1.2)
- `local-docs/project-requirements/functional-requirements/fr029-payment-system-config/prd.md` (buffer window addition)
- `local-docs/project-requirements/system-prd.md` (FR-017 payout schedule wording)

## Summary

Applied 9 fixes from FR-017 verification report. Fixes address constitution compliance, internal consistency, missing dependencies, and cross-FR alignment.

## Changes Applied

### Critical Fixes

1. **Integration 5 — Shared Database → API** (Constitution Principle I violation)
   - **Before**: Integration 5 specified "Provider platform queries shared database for payout history (read-only views)"
   - **After**: Replaced with API-based integration referencing REQ-017-027, enforcing multi-tenant boundary per Constitution Principle I ("No direct database access across tenant boundaries")

2. **5 Missing Dependencies Added**
   - Added FR-006 (Booking & Scheduling — refund policy), FR-018 (Affiliate Management — commission calc/payout), FR-029 (Payment System Config — Stripe, currency, buffer window), FR-030 (Notification Rules — payment reminders), FR-032 (Provider Dashboard — navigation shell, bank accounts)
   - Each entry includes "Why needed" and "Integration point"

### Medium Fixes

3. **Commission Column Rename (Screens 7-8)**
   - Renamed "Commission %" to "Commission" in provider-facing Screens 7 and 8
   - Added note that the field stores both commission model type (Percentage or Flat Rate) and value, displayed contextually

4. **Secondary Approval Threshold Standardized**
   - User Story 6 scenario updated from ">£1,000" to ">£10,000" to match Security Considerations definition

5. **Dynamic Currency Pair Clarification**
   - Removed "MVP supports two currency pairs only: USD/GBP and USD/TRY" from Business Rule 4 and Fixed in Codebase section
   - Replaced with reference to FR-029 as the authority on supported currency pairs (dynamic, admin-configurable)
   - Updated B2 (Currency Alert) workflow from hardcoded pairs to "all configured currency pairs (FR-029)"

6. **Payout Buffer Window — Added to FR-029**
   - Added buffer window setting to FR-029 Admin Editability Rules (default: 3 days, range: 1–7 days)
   - Added Payout Rule 1 to FR-029 Payment & Billing Rules section
   - FR-017's reference to FR-029 for buffer window config is now properly defined

### Minor Fixes

7. **Conversion Rate Data Provenance**
   - Added "Inquiries count sourced from FR-003 / P-02: Quote Request & Management" to Screen 5 field description

8. **System PRD Payout Schedule Updated**
   - Changed "bi-weekly or monthly" to "weekly, bi-weekly/2x a month, or monthly — per provider agreement"
   - Aligns with FR-017 PRD and client transcription evidence

9. **Assumption 7 Reworded**
   - Acknowledged S-06 (Audit Log Service) from constitution; MVP uses database logs, S-06 integration planned for post-MVP

## Decisions Made

| Decision | Chosen Option | Rationale |
|----------|--------------|-----------|
| Integration 5 fix | Remove and reference REQ-017-027 | Cleanest fix; REQ-017-027 already defines the correct approach |
| Missing dependencies | Add all 5 | Complete coverage; all are heavily referenced in PRD body |
| Commission column | Rename to "Commission", note dual model | Accommodates Flat Rate without splitting into multiple columns |
| Approval threshold | £10,000 | Reduces admin friction; still covers high-value cases |
| Currency scope | Dynamic pairs via FR-029 | FR-029 already supports configurable pairs; FR-017 shouldn't restrict |
| Buffer window home | FR-029 Admin Editability | Natural fit alongside other billing config settings |
| Conversion Rate source | FR-003 provenance note | Minimal, clear fix |
| System PRD schedule | Add weekly option | Validated by client transcription |
| Assumption 7 | Acknowledge S-06 | Constitution-aware without changing MVP approach |
