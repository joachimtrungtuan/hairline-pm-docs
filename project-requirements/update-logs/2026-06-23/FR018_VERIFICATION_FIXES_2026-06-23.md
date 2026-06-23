# FR-018 Verification Fixes (v1.7 → v1.8 → v1.9 → v2.0)

**Date**: 2026-06-23
**FR**: FR-018 — Affiliate Management
**Author**: Claude (Opus 4.8)
**Trigger**: `verify-fr FR-018` verification report; fixes applied per Product Owner decisions

---

## Summary

Tracks three FR-018 verification-fix passes applied on 2026-06-23. Pass 1 (v1.8) resolved the original 1 critical, 3 medium, and 2 minor issues and aligned one `system-prd.md` requirement line. Pass 2 (v1.9) resolved the follow-up status, margin-guard, and currency-note issues. Pass 3 (v2.0) resolved the remaining payout ownership, shared-screen routing, and marketing-materials coverage issues.

## Changes

### 1. Audit-trail retention → 10 years (Critical — constitution compliance)

- Constitution (Principle II / Data Retention, L645) mandates audit trails be retained **10 years**; the PRD had set them at 7 years.
- Updated: **Audit Rule**, **REQ-018-018**, the **Fixed-in-Codebase** entry, and the B3/B5 retention notes to specify a 10-year immutable audit trail. Financial/payout records remain at the 7-year minimum.

### 2. Commission base → % of booking revenue (Medium — financial correctness)

- The PRD modelled percentage commission inconsistently: User Story 3 used 15% of **revenue** ($750 on $5,000) while User Story 5 used 15% of **Hairline commission** ($22.50 on $1,000).
- **Decision (Product Owner)**: commission percentage is **% of booking revenue**, not of Hairline's commission — matching client intent ("10% to the user, 10% to the affiliate") and US3.
- Updated: Commission Type/Percentage fields on Screens 2 and 3.2, the Screen 2 preview ("$150"), Main-Flow and Fixed-in-Codebase wording, **new Rule 14 (Commission base)**, and the worked examples in User Story 3 and User Story 5 ($150, reversal $150). Commission remains funded from Hairline's commission, never the provider payout.
- **Cross-doc**: `system-prd.md` FR-018 requirement line changed from "% of platform commission" to "% of booking revenue … funded from Hairline's commission".

### 3. Commission bounds tightened (Medium)

- Percentage range **5-50% → 5-25%**; fixed-amount **min $10 → min $50**; high-rate warning threshold **>30% → >20%** (Screens 2 and 3.2). Now consistent with Business Process Assumption 2 (5-25% / $50-$200) and the client transcription ("20% is quite high", "£50, £200").

### 4. Performance Tier & Campaign Eligibility defined (Medium)

- Added a new **Affiliate Segmentation Rules** subsection defining Performance Tier bands (Bronze/Silver/Gold/Platinum by trailing-12-month revenue) and Campaign Eligibility criteria (Active status, completed activation, complete payout details), making Screen 1's eligibility gating and filters testable.

### 5. Masking wording standardized (Minor)

- Privacy Rule 2 and REQ-018-016 changed "last 4 **characters**" → "last 4 **digits**", matching the standard used for bank/payment fields across other FRs (e.g., FR-029, FR-017).

### 6. Payout schedule fixed at monthly-on-the-7th (Minor)

- Per the client transcription ("we'll only have the monthly option", paid "on the seventh of every month"), removed all "configurable date / 1-28 / 30-day notice" language. Payout schedule is now stated as **fixed**, moved to Fixed-in-Codebase, and the Screen 2 field is read-only display.

## Files Changed

- `local-docs/project-requirements/functional-requirements/fr018-affiliate-management/prd.md` (v1.7 → v1.8)
- `local-docs/project-requirements/system-prd.md` (FR-018 commission requirement line)

---

# FR-018 Verification Fixes — Pass 2 (v1.8 → v1.9)

**Date**: 2026-06-23
**FR**: FR-018 — Affiliate Management
**Author**: Claude (Opus 4.8)
**Trigger**: Second `verify-fr FR-018` pass; fixes applied per Product Owner decisions (Issue 1 → Opt 1, Issue 2 → Opt 1, Issue 3 → Opt 1)

## Summary

Resolved the 2 medium and 1 minor issues surfaced by the second verification pass, including the v1.8 Finance follow-up below.

## Changes

### 1. Initial affiliate Status = "Pending" reconciled (Medium — intra-document contradiction)

- Main Flow (step 5), Screen 1, and Rule 12 set the initial `Status` to **"Pending"** until the password is set; Screen 2, Screen 10, and Screen 10.1 instead said `Status = "Active"` on create, contradicting them.
- **Decision**: adopt **"Pending" on create** (Option 1). Updated the Screen 2 Activation State rule, Screen 10 Activation State rule, and Screen 10.1 On-Success rule so account creation sets `Status = "Pending"` / `Activation Status = "Invited"`, and completing set-password flips **both** to "Active" (per Rule 12).

### 2. Per-booking Hairline-funded cost ceiling added (Medium — financial correctness)

- No rule prevented the patient discount (≤30%) plus affiliate commission (≤25% of booking revenue), both Hairline-funded, from exceeding Hairline's own commission on a booking (~10% per transcription). Assumption 4 only caps aggregate program cost, not per-booking margin. **This resolves the v1.8 Finance follow-up.**
- **Decision**: add a validation rule (Option 1). Added **Rule 15 (Hairline-funded cost ceiling)**, a **Screen 4 Margin Guard** business rule and **AC-6**, and **REQ-018-041**: percentage breaches (`discount % + commission % > Hairline's commission %`) are **blocked** (override requires documented, audited business approval); fixed-amount configs raise a **review warning** (booking-value dependent).

### 3. Currency figures clarification (Minor)

- Added a note to the **Currency Rule** stating that client GBP figures ("£50", "£200") are illustrative; USD literals (e.g., $50 minimum fixed commission, $50 payout threshold) are stated in the platform base currency (USD, per FR-029) and are not a direct GBP→USD conversion.

## Files Changed

- `local-docs/project-requirements/functional-requirements/fr018-affiliate-management/prd.md` (v1.8 → v1.9)

## Follow-ups / Notes

- v1.8 Finance follow-up (per-booking margin) is **resolved** by Rule 15 / REQ-018-041 above. Finance still owns the choice of the percentage-cap / fixed-amount defaults the guard enforces against Hairline's commission rate.

---

# FR-018 Verification Fixes — Pass 3 (v1.9 → v2.0)

**Date**: 2026-06-23
**FR**: FR-018 — Affiliate Management
**Author**: Codex
**Trigger**: Third `verify-fr FR-018` follow-up; fixes applied per Product Owner decisions (Issue 1 → Option 1, Issue 2 → Option 1, Issue 3 → Option 1)

## Summary

Resolved the remaining 1 critical and 2 medium issues from the v1.9 verification report by moving payout execution back to FR-017 / A-05, correcting stale shared-screen routing, and satisfying the system-PRD marketing-materials feature as read-only affiliate access.

## Changes

### 1. Payout execution moved out of FR-018 (Critical — dependency ownership)

- **Decision**: Option 1 — keep FR-018 payout surfaces read-only/export only; FR-017 / A-05 owns affiliate billing, payout approval/retry, and Stripe transfer execution.
- Updated Screen 7 to **Affiliate Payout Status & History**, removed Screen 7.1 from FR-018 scope, and made Screen 8 read-only for payout details/receipts.
- Rewrote B2, Integration 3, User Story 4, REQ-018-008, REQ-018-021, REQ-018-035, and Entity 4 so FR-018 calculates/exposes payout data and reads status back from FR-017 rather than initiating transfers.

### 2. Screen 3 route mismatch corrected (Medium — internal consistency)

- **Decision**: Option 1 — correct the table links.
- Screen 3 now states assigned promo-code rows link to **Screen 6** and payout-history rows link to **Screen 8**, matching the existing business rules and acceptance criteria.

### 3. Marketing-material access added (Medium — system PRD coverage)

- **Decision**: Option 1 — add read-only affiliate access to marketing materials.
- Added read-only externally hosted marketing-material links to Screen 9.2 and clarified that asset creation, editing, approval, and hosting remain outside FR-018 scope.
- Added **REQ-018-042**, an external-materials dependency note, and `Marketing Material Links` on the Discount Code entity.

### 4. Payout-boundary wording cleanup (Medium follow-up — Issue 1 / Option 1)

- Cleaned up residual FR-018 wording that implied payout execution ownership, replacing it with payout-cycle calculation, review, handoff, and read-only status/history language.
- Removed the stale `Screen 7.1` tenant-scope reference and aligned shared-service labels to **S-02 / S-03 / S-06** so payment execution remains clearly owned by **FR-017 / A-05**.

## Files Changed

- `local-docs/project-requirements/functional-requirements/fr018-affiliate-management/prd.md` (v1.9 → v2.0 → v2.1)
