# FR-019 Screen Specifications Restructure + FR-004 Alignment

**Date**: 2026-05-12
**Documents**:
- `local-docs/project-requirements/functional-requirements/fr019-promotions-discounts/prd.md` (v1.3 → v1.5)
- `local-docs/project-requirements/functional-requirements/fr004-quote-submission/prd.md` (v1.7 → v1.8)

**Author**: Claude (Opus 4.7)

---

## Summary

Major restructure of the Screen Specifications section in FR-019 (Promotions & Discount Management). The previous specification covered only three screens at a high level (admin create/manage, provider approvals + setup, patient apply) plus a finalised Screen 4 catalog. The new specification introduces a unified three-program model and expands the inventory to 11 type-aware screens spanning all three platforms.

---

## Three-Program Model

Introduced `PromotionProgram` as the unified parent entity with `program_type`:

1. **`ADMIN_VIA_PROVIDER`** — Admin defines campaign affecting both Hairline and provider fees; targeted providers must opt-in before the code is selectable on their quotes.
2. **`PROVIDER_SELF`** — Provider defines a discount affecting only their own fees; no admin approval required.
3. **`HAIRLINE_FUNDED_DIRECT_ISSUED`** — Admin defines a Hairline-funded discount issued directly to patients via open-entry codes, segment-binding, affiliate distribution (FR-018), or individual issuance.

Admin retains override authority on every record across all three program types.

---

## New Screen Inventory (11 screens)

### Admin Platform (A-06) — 6 screens

1. **Promotion Program Hub** — Unified catalog with program-type filter (expands prior Screen 4)
2. **Promotion Detail (Create / Edit)** — Type-aware form (expands prior Screen 1)
3. **Provider Adoption Manager** — Per-program list of provider opt-in status with admin override
4. **Provider Promotion Portfolio** — Per-provider drill-down across adopted-admin + self-created programs
5. **Hairline-Funded & Direct-Issued Codes Manager** — Specialized manager for Program Type 3
6. **Promotion Analytics & Applications** — Merged Overview (KPIs, ROI, funnel) + Applications log; preserves client's Applied vs Completed state distinction

### Provider Platform (PR-02 / PR-05) — 4 screens

7. **Admin Campaigns** — Inbox (Pending) + Adoptions (Active) + Past (split from prior Screen 2)
8. **My Promotions (List)** — Provider's self-created promotions
9. **Promotion Detail (Create / Edit) — Provider** — Form for self-created promotions
10. **Promotion Analytics & Applications** — Provider mirror of Screen 6 with quote/case removal/replace control

### Patient Platform (P-03 overlay) — 1 screen

11. **Apply Discount at Quote / Booking** — Retains prior Screen 3 with explicit Discount Scope label (which fee component the discount applies to) per HairlineApp Part 1 L156–158.

---

## Transcription Alignment

### Confirmed against transcriptions

- Admin all-promotions view, funding-model display, code field, max-use, validity (Admin Part 1 L277–330)
- Applied vs Completed distinction preserved as explicit redemption states (Admin Part 1 L333–344)
- Provider approval inbox with accept/decline + post-acceptance display (Provider Part 2 L11–21)
- Provider can edit/delete own discounts (Provider Part 2 L21)
- Patient code entry with breakdown showing which component is discounted (HairlineApp Part 1 L149–158)
- Both Fees and Hairline Only funding paths (Provider Part 1 L113–125, Part 2 L3–8)

### Deliberate scope expansions beyond transcriptions

Two extensions were made knowingly with user approval and are flagged in-screen:

1. **Admin visibility into provider self-created discounts** (Screen 1 filter + Screen 4 Portfolio). The client transcription (Admin Part 1 L295–300) stated admin would "never going to pick them or change them or amend them in reality" and concluded "we probably don't need to see those." The new specification adds this visibility to give admin governance authority over the full promotion system, including the ability to pause or archive provider self-created programs via row action with mandatory reason text. Editing of provider self-created programs by admin remains an override action, logged in audit.

2. **Optional Code field on provider self-created promotions** (Screen 9). The client transcription (Provider Part 2 L27–33) stated that discount codes are not relevant for provider self-created discounts because providers select them from a list during quote creation. The new specification retains the field as **optional** so providers may also issue code-based promotions for marketing distribution (e.g., flyer codes, partner promos). The default `Application Mode` is `List-selection during quote`, matching the transcribed intent; `Code-only` and `Either` modes are additional opt-in capabilities.

---

## Other Document Changes

- **Business Workflows**: Added Alt Flow C1 (Hairline-Funded / Direct-Issued Code Redemption).
- **Key Entities**: Replaced the four-entity model with `PromotionProgram`, `PromotionCode`, `Adoption`, `Application`, `ReportSnapshot`; added explicit fields for program_type, application_mode, applies_to, funding_split, and the Applied/Completed state lifecycle.
- **Change Log**: Added v1.4 entry documenting the restructure and the two scope expansions.
- **Last Updated**: 2026-04-13 → 2026-05-12.

---

## Downstream Impact

- **FR-022 (Search & Filtering)**: Search and filter field definitions on Screen 1 are co-owned with FR-022; FR-022 may need a corresponding update to add Program Type and Funding Model to the discount filter contract.
- **FR-018 (Affiliate Management)**: Screen 5 (Hairline-Funded & Direct-Issued Codes Manager) references affiliate-bound issuance channels that integrate with FR-018; verify affiliate-id binding and incentive accrual contract alignment.
- **FR-017 (Billing & Finance)**: Screen 6 Reverse/Refund/Void actions emit reconciliation events to FR-017; verify event contract.
- **FR-031 (Admin RBAC)**: All admin override actions on Screens 3, 4, 5, 6 require RBAC enforcement; verify roles are defined for force-revoke, force-archive, refund, void.
- **FR-014 (Provider Analytics)**: Provider Screen 10 overlaps with FR-014 dashboards; verify whether promotion analytics live in FR-019 module or surface via FR-014 with cross-link.

These downstream verifications are recommended next-step actions but were not performed in this update.

---

---

## FR-004 Alignment (v1.5 of FR-019 + v1.8 of FR-004)

After the v1.4 restructure, the user flagged that FR-004 (Quote Submission) Screen 1 already anticipates two modes for provider promotion attachment on a quote: (a) select from list of existing reusable promotions, (b) create on-the-spot. The v1.4 rewrite missed this surface entirely and only specified pre-defined provider promotions managed from the standalone Screen 9.

### Resolution

FR-019 was extended (v1.5) and FR-004 was tightened (v1.8) to formalize the two modes as `PromotionProgram.scope`:

| Mode | FR-019 Screen 9 Entry Point | `PromotionProgram.scope` | `quote.promotionId` |
|------|----------------------------|--------------------------|--------------------|
| **M1 — Select Existing** | Standalone (PR-02 / PR-05 nav) | `REUSABLE` | Set to existing program id |
| **M2 — Inline Structured Create** | Modal from FR-004 Screen 1 | `AD_HOC_QUOTE_BOUND` (with `bound_quote_id`), promotable to `REUSABLE` via "Save as reusable" toggle | Set to new program id created inline |

The previously-supported third mode — free-text `quote.promotionNote` — was **dropped**. Tighter governance: every discount applied on the platform must correspond to a tracked `PromotionProgram` record.

### FR-019 v1.5 changes

- `PromotionProgram` entity gains `scope` (`REUSABLE` | `AD_HOC_QUOTE_BOUND`) and `bound_quote_id`.
- Screen 1 Hub adds a Scope filter.
- Screen 9 redesigned with two entry modes; Mode 2 defaults `total_usage_limit = 1` unless "Save as reusable" is toggled.
- Alt Flow A1 split into A1a (pre-defined reusable) and A1b (inline ad-hoc).
- New business rule: free-text promotion notes are not supported.

### FR-004 v1.8 changes

- Screen 1 Promotion field type: `select/text` → `select-or-create`. Validation tightened to require resolution to a structured `PromotionProgram` id.
- Screen 3 and Screen 5 Promotion field type: `text/select` → `reference` (read-only resolution).
- Screen 7 Admin Inline Edit Promotion field documented for admin override with inline-create permitted.
- Quote entity: `promotionNote` field **removed**.

### Downstream impact of M3 removal

- Any existing quote records that have `promotionNote` set (free-text discount annotations) would need a data migration. The FR does not mandate a migration approach — that decision sits with implementation. Two options for the migration: (a) materialize each populated `promotionNote` as an `AD_HOC_QUOTE_BOUND` PromotionProgram with name = first 120 chars of the note, or (b) preserve historical `promotionNote` values in an audit-only field and disallow new entries.
- Should be flagged to implementation when FR-004 / FR-019 enter task creation.

---

## Files Changed

- `local-docs/project-requirements/functional-requirements/fr019-promotions-discounts/prd.md` (major restructure v1.4 + FR-004 alignment v1.5)
- `local-docs/project-requirements/functional-requirements/fr004-quote-submission/prd.md` (v1.8: Promotion field retypes across Screens 1/3/5/7, Quote entity `promotionNote` removed, change log v1.8 added)
- `local-docs/project-requirements/update-logs/2026-05-12/FR019_SCREEN_SPECIFICATIONS_RESTRUCTURE_2026-05-12.md` (this file, new)
- `local-docs/project-requirements/update-logs/README.md` (indexed)

---

## FR-019 v1.6 Verification Fixes (2026-05-12)

Five issues resolved from post-verification review:

- **B2 / B3 split**: B2 scoped to user-initiated conflict (prompt to choose); new B3 added for auto-applied conflict (silent priority order: patient > provider > affiliate). Business Rules updated to reference both flows.
- **Dependencies completed**: Added FR-004, FR-018, FR-022, FR-031, FR-010 to the Internal Dependencies section with one-line integration descriptions.
- **Screen 2 AC-4**: Added negative-path acceptance criterion rejecting `Auto-applied` mode on Admin-via-Provider (Both-Fees) programs.
- **PromotionCode status renamed**: `reserved` → `in-progress` in Screen 5 codes table, Screen 6 redemption funnel, and Key Entities; added disambiguation note explaining that `PromotionCode.status = in-progress` and `Application.state = APPLIED` describe the same moment from different entity perspectives.
- **Screen 2 Notes**: Added one-line explanation of why Application Mode option sets differ between admin and provider forms.
