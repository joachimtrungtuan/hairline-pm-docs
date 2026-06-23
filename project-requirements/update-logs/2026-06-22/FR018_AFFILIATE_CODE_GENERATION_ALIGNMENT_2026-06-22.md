# FR-018 Affiliate Code Generation Alignment

**Date**: 2026-06-22
**Documents**:
- `local-docs/project-requirements/functional-requirements/fr018-affiliate-management/prd.md` (v1.0 → v1.2)
- `local-docs/project-requirements/functional-requirements/fr019-promotions-discounts/prd.md` (v1.8 → v1.9)
- `local-docs/project-requirements/functional-requirements/fr022-search-filtering/prd.md` (v2.10 → v2.11)

**Author**: Codex

---

## Summary

Aligned affiliate promo-code ownership so FR-018 is the source of truth for affiliate-specific code generation, assignment, dashboard visibility, and payout attribution. FR-019 remains the shared promotion engine for validation, active windows, usage limits, applied/completed redemption lifecycle, and financial-impact logging.

---

## FR-018 Updates

- Added filtered bulk affiliate code generation: admins can select affiliates manually or by filters such as country/region, affiliate type, language, performance tier, campaign eligibility, and payout setup completeness.
- Defined the core attribution rule: bulk generation creates one distinct unique promo code per affiliate; one shared affiliate payout code across multiple affiliates is not supported.
- Added Screen 1 acceptance criteria, Screen 3 acceptance criteria, and Screen 6 dashboard acceptance criteria to align with verified PRD screen-spec conventions.
- Restructured Screen Specifications into tenant/platform subsections using the verified PRD convention: Admin Platform Screens and Affiliate Platform Screens, with Patient Platform and Provider Platform clarified as out of scope for this FR.
- Updated Screen 3 from generic discount-code management to affiliate code management with generation modes: Single Affiliate, Selected Affiliates, and Filtered Segment.
- Clarified that generated active codes appear immediately in the assigned affiliate's dashboard with campaign name, active window, status, and per-code performance breakdown.
- Added business rules, success criteria, dependencies, integration notes, user story, edge cases, requirements, and key entities for bulk code generation.

---

## FR-019 Updates

- Added an explicit scope-boundary note: affiliate-specific promo-code generation, bulk affiliate assignment, dashboard display, and payout attribution are owned by FR-018 / A-07.
- Clarified that affiliate-bound codes registered into FR-019 are managed by FR-019 for validation and redemption state only.
- Updated the Screen 5 business rule for affiliate-bound codes to preserve FR-018 ownership of generation and one-affiliate-per-code assignment.

---

## FR-022 Updates

- Synced the A-07 Affiliate Management filter inventory with FR-018 Screen 1.
- Added country/region, affiliate type, language, performance tier, campaign eligibility, and payout setup filters to support affiliate cohort selection before bulk code generation.

---

## Implementation Guidance

- Do not implement one shared affiliate payout code for multiple affiliates.
- For public non-attributed marketing campaigns, use FR-019 open Hairline-funded codes.
- For affiliate campaigns, generate distinct affiliate-bound codes through FR-018 and register them into FR-019 for validation/redemption.

---

## Files Changed

- `local-docs/project-requirements/functional-requirements/fr018-affiliate-management/prd.md`
- `local-docs/project-requirements/functional-requirements/fr019-promotions-discounts/prd.md`
- `local-docs/project-requirements/functional-requirements/fr022-search-filtering/prd.md`
- `local-docs/project-requirements/update-logs/2026-06-22/FR018_AFFILIATE_CODE_GENERATION_ALIGNMENT_2026-06-22.md`
- `local-docs/project-requirements/update-logs/README.md`
