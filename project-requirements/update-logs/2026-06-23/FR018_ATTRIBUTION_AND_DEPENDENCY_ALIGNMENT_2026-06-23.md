# FR-018 Attribution and Dependency Alignment

**Date**: 2026-06-23
**FR**: FR-018 - Affiliate Management
**Author**: Codex
**Trigger**: Follow-up decisions after `verify-fr FR-018` report

---

## Summary

Applied Product Owner decisions for the two remaining FR-018 verification issues:

1. Affiliate referral attribution must be preserved separately from the final price-discount priority because provider-side promotions can be applied outside the patient's knowledge.
2. Stale FR-019 and FR-022 dependency references should be patched directly.

## Changes

### 1. Affiliate attribution separated from final price discount

- Updated FR-018 Rule 11 so a valid captured affiliate-bound code or affiliate auto-apply referral link can still earn affiliate referral credit and commission after payment-confirmed booking completion, even when a higher-priority patient/provider discount controls the patient's final price.
- Updated FR-018 referral-count wording, REQ-018-003, REQ-018-010, Integration 2 payload, edge-case wording, and the booking entity from "Booking with Affiliate Code" to "Booking with Affiliate Attribution".
- Updated FR-017's affiliate-vs-provider discount edge case so the provider promotion can win the patient-facing price discount while the affiliate attribution is preserved for FR-018 commission output and FR-017 payout execution.
- Updated FR-019's auto-applied conflict outcome so price-discount priority does not erase valid affiliate attribution metadata.

### 2. Stale dependency references fixed

- Updated FR-019's affiliate-bound bulk-generation acceptance criterion from "all bound to the affiliate" to one unique code per selected affiliate.
- Updated FR-022's affiliate payout search/filter mapping from stale `FR-018 / Screen 5` to current `FR-018 / Screen 7: Affiliate Payout Status & History`.

## Files Changed

- `local-docs/project-requirements/functional-requirements/fr018-affiliate-management/prd.md` (v2.2 -> v2.3)
- `local-docs/project-requirements/functional-requirements/fr017-admin-billing-finance/prd.md` (v2.1 -> v2.2)
- `local-docs/project-requirements/functional-requirements/fr019-promotions-discounts/prd.md` (v1.9 -> v2.0)
- `local-docs/project-requirements/functional-requirements/fr022-search-filtering/prd.md` (v2.11 -> v2.12)

## Notes

- This update intentionally changes the earlier FR-018 v1.7 "code-based attribution only when final discount applied" policy. The current approved model is: one final discount controls price, but affiliate referral attribution can remain independent for commission fairness.
- Minor follow-up from the subsequent `verify-fr FR-018` pass: rewrote the FR-017 dependency bullet in FR-018 so it describes payout execution/reconciliation ownership only, and added a correction note to the stale v1.7 change-log row pointing readers to the v2.3 attribution model.
