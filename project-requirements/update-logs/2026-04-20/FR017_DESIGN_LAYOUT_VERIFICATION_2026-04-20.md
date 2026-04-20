# FR-017 Design Layout Verification — 2026-04-20

**Date**: 2026-04-20
**Type**: Design Layout Verification
**Scope**: FR-017 Admin Billing & Financial Management — full scope (`F1` through `F8`)
**Report**: `local-docs/reports/2026-04-20/design-layout-verification-fr017.md`

---

## Summary

Verified the full FR-017 layout scope against the current `layout-temp/` asset set, covering:

- `F1` Revenue Dashboard & Reporting
- `F2` Provider Payout Processing
- `F3` Patient Billing & Refund Management
- `F4` Discount Usage Tracking
- `F5` Affiliate Billing & Commission Payouts
- `F6` Transaction Search & Audit
- `F7` Currency Alert Response
- `F8` Provider Earnings & Payout History

This pass confirms that the admin-side financial suite is mostly designed, and after the latest F8 recheck the provider-facing finance scope now has layout coverage for both Screen 9 and Screen 10, though Screen 10 is still only partially covered because the delivered files show a payout-detail state rather than the full payout-history list.

## Overall Verdict

**Mixed result**:

- `F1` Revenue Dashboard & Reporting → **🟢 COMPLETE**
- `F2` Provider Payout Processing → **🟡 PARTIAL**
- `F3` Patient Billing & Refund Management → **🟡 PARTIAL**
- `F4` Discount Usage Tracking → **🟢 COMPLETE**
- `F5` Affiliate Billing & Commission Payouts → **🟡 PARTIAL**
- `F6` Transaction Search & Audit → **🟡 PARTIAL**
- `F7` Currency Alert Response → **🟢 COMPLETE**
- `F8` Provider Earnings & Payout History → **🟡 PARTIAL**

Screen-level result:

- 12 of 12 required screens now have mapped layout coverage
- Screen 9 maps to the `provider-earnings/` layout set and Screen 10 now maps to the `payout-history/` layout set, but Screen 10 still lacks the parent payout-history list view

## Key Findings

1. **Core admin billing surfaces are present, but several execution-critical states still drift from the FR.**
   - Provider payout batch confirmation has a count mismatch and uses a routed detail page where the FR specifies a modal.
   - Patient invoice detail is missing the required prominent `At Risk` banner and does not evidence the explicit `Close` action.
   - Affiliate billing includes the expected list/detail/modals, but its main list is still titled `Provider Billing` and the bulk-payout total is inconsistent between list and modal.

2. **Investigation and alert tooling are largely implementation-ready.**
   - Transaction Search includes the search table, no-results state, dispute panel, and complete audit-log table.
   - Currency Alert includes the required alert summary, affected-bookings table, and admin decision controls.
   - The main follow-up issue in investigation tooling is a mislabeled mandatory `Internal Note` textarea inside the dispute panel.

3. **Provider-facing financial history is now covered for both stages, but Stage 2 is still incomplete.**
   - The `provider-earnings/` layouts cover Screen 9 and align well with the Stage 1 earnings-tracker requirements, including summary cards, earnings rows, refund-adjustment markers, payout-status variants, export, and filters.
   - The new `payout-history/` layouts cover a selected payout-detail state for Screen 10, including payout summary, failure banner, treatment breakdown, copy-reference CTA, and retry-resolution history.
   - The missing part of Screen 10 is the parent payout-history list with multiple payout rows, filters, sorting, and a paid-state invoice-download variant.

## Follow-Up Actions

1. Fix the provider payout batch summary mismatch and decide whether Screen 3 remains a routed page or returns to the FR-defined modal pattern.
2. Add the required `At Risk` banner and explicit close action to the patient invoice detail state.
3. Rename the affiliate list title to `Affiliate Billing` and synchronize the bulk-payout amount shown in the confirmation flow.
4. Rename the dispute-panel textarea to `Internal Note`.
5. Add the parent Screen 10 payout-history list plus a paid-state invoice-download variant, and add visible sort controls plus linked booking references to Screen 9.

## Traceability

- Full report: `local-docs/reports/2026-04-20/design-layout-verification-fr017.md`
- Requirement source: `local-docs/project-requirements/functional-requirements/fr017-admin-billing-finance/prd.md`
