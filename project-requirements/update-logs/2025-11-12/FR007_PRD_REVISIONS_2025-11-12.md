# FR-007 PRD Revisions - November 12, 2025

Scope: Capture substantive FR-007 updates completed prior to final verification (versions 1.1 through 1.4).

## Summary of Changes

- **Version 1.1**
  - Clarified that commission rates and deposit defaults are centrally managed in `FR-029: Payment System Configuration`.
  - Explicitly delegated provider payout execution and invoice management to `FR-017: Admin Billing & Financial Management`.
  - Tied refund amount calculations to `FR-006` cancellation policy.
  - Reworked tenant breakdown notes to reflect configuration ownership.
  - Added patient payment progress visibility for provider/admin screens.

- **Version 1.2**
  - Expanded provider-facing screens to aggregate inquiry, quote, booking, and payment data (continuity across FR-003 → FR-006).
  - Enhanced `Screen 3: Booking Payment Status & Progress (Provider)` with anonymized identifiers, payment statuses, and overlap safeguards.
  - Enriched `Screen 4: Provider Payout Overview` with payout readiness, commission, and dependency references to FR-017.

- **Version 1.3**
  - Added `Screen 5B: Payment Detail View (Admin)` consolidating patient journey data (inquiry through payment) for finance ops.
  - Upgraded `Screen 6: Refund Processing (Admin)` with contextual sections (booking, patient, treatment, payment summary, refund breakdown).
  - Linked dashboard actions to detailed views, aligning workflow with FR-006 booking detail structure.

- **Version 1.4**
  - Removed redundant read-only configuration screen; replaced with explicit link-outs to `FR-029`.
  - Added configuration note under Admin Platform clarifying separation of duties.
  - Ensured change log reflects configuration streamlining.

## Consistency Checks

- Cross-referenced with `system-prd.md` FR-007 scope for deposits, refunds, commissions, and payouts.
- Validated screen data requirements against client transcriptions (`HairlineApp-Part1`, `Hairline-ProviderPlatformPart1`, `Hairline-AdminPlatform-Part1`).
- Confirmed dependencies and RBAC notes align with FR-006, FR-017, and FR-029 responsibilities.

## Impact

- FR-007 now provides comprehensive payment lifecycle coverage across tenants with clear dependency mapping.
- Admin and provider experiences expose the full financial trail without duplicating configuration surfaces.
- Sets the stage for final verification and approval (captured separately in `FR007_PRD_VERIFIED_2025-11-12.md`).
