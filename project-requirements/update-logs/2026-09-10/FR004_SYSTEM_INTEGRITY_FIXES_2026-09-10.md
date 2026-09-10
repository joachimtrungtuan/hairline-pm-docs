# FR-004 System Integrity Verification Fixes

**Date**: 2026-09-10
**Type**: FR verification follow-up and cross-document reconciliation
**Scope**: FR-004 PRD v2.4, CR-FR004-20260909-01, `system-data-schema.md`
**Trigger**: Second verification pass on FR-004 after the 2026-09-09 parent-quote/package-options restructure, focused on whether surrounding system documents still hold together with the new aggregate.

---

## Summary

The FR-004 aggregate itself verified clean: the Quote Data Ownership Matrix covers every Screen 1 field with exactly one owner, schema tables 7A–7D match the option model, and Constitution principles VI (Data Integrity & Audit Trail) and X (Versioning & Change Management) pass. The defects found were in the documents around FR-004 — a stale quote status enum, three structures that exist in code but not in the schema doc, an un-deprecated discount column, a Change Request whose metadata lagged the PRD, and an admin edit surface that could produce invalid option items.

Two findings were explicitly deferred by the Product Owner and are **not** addressed here: downstream FR-005/FR-008 option-awareness, and the `system-prd.md` FR-005 acceptance wording. Both remain open.

---

## Changes Applied

### 1. Quote status enum corrected (`system-data-schema.md`, table 7)

The `quotes.status` column and its Status Values / Status Triggers blocks listed `inquiry, quote, accepted, confirmed, inprogress, aftercare, completed, rejected, cancelled`. Backend source confirms those are **treatment case statuses** stored on `inquiries.status`, not quote statuses — see `Inquiry.php` status constants and its quote-to-inquiry status map. The schema doc, not FR-004, was stale.

Replaced with the eight FR-004 quote statuses plus `confirmed` as the FR-006 payment bridge, with matching triggers, and added two notes:

- **API divergence**: the column stores `sent` while `Quote::getStatusAttribute()` returns `quote` to clients, with the mutator converting back on write. This divergence existed in code but was undocumented anywhere.
- **Case lifecycle is separate**: the two enums MUST NOT be merged.

Historical conversion evidence: migration `2026_07_07_140000_align_quote_statuses_with_prd.php`, which also split the legacy single `cancelled` value into `cancelled_other_accepted` and `cancelled_inquiry_cancelled`.

### 2. Undocumented structures added (`system-data-schema.md`)

Three structures existed in the implementation but had no schema documentation:

- **7E. Quote Clinicians** (`quote_clinicians`) — was listed in the table inventory with no definition. Now defined.
- **7F. Quote Documents** (`quote_documents`) — quote-level attachments, entirely absent from the doc. Now defined and added to the inventory.
- **`quotes.graft_visual_plan_url`**, plus `treatment_plan_validated` and `expiry_calculated_at`, added to the `quotes` column table.

### 3. Real spec gap flagged (`system-data-schema.md`, table 7)

`common_requirements` — required by REQ-004-020 — exists in **neither** the schema doc nor the implementation. Recorded as an explicit Spec Gap note rather than silently documenting a column that does not exist. REQ-004-020 cannot be marked implemented until it is added.

### 4. Discount ownership resolved (`system-data-schema.md`, table 7)

`quotes.discount_id` was the only surviving parent-level discount owner after discounts moved to `quote_options`. Marked **DEPRECATED (FR-004 v2.3)** in the same style as `package_id`, `treatment_date`, and `quote_amount`, removing the two-owners ambiguity.

### 5. Admin inline edit aligned with option validation (`prd.md`, Screen 7)

The Screen 7 admin inline-edit table let an admin add an option item with only name, description, and cost — omitting Item Type, Included, and Item Order, which Sub-screen 2A requires. An admin could therefore create an option item that fails option-snapshot validation.

- Row renamed **Custom Services → Option Items** and its validation aligned with Sub-screen 2A.
- **Estimated Grafts** row now states that saving a new value regenerates Graft Description from the approved template and does not preserve the prior text.

### 6. Commission wording (`prd.md`, Quote Data Ownership Matrix)

Restated from "read-only amount/rate" to "read-only rate (percentage)", matching `quotes.commission INTEGER` (a percentage, not an amount).

### 7. Change Request metadata reconciled (`change-request-2026-09-09-quote-options-model.md`)

- Version change `v1.9 → v2.2` corrected to `v1.9 → v2.4`, with each version's role named.
- Target REQ range corrected from `REQ-004-014 through REQ-004-029` to `through REQ-004-030`; the conflicting second range in the affected-contracts list corrected to match.
- Change-log traceability extended to v2.3 and v2.4; approval line records the 2026-09-10 amendment.
- The blanket claim that system documents "require later controlled reconciliation" replaced with what is actually done (system PRD FR-004 section; schema tables 7 and 7A–7F) versus still open (system technical specification; system PRD FR-005 acceptance wording).

---

## Open Items (deferred by decision, not oversight)

| Item | Status | Note |
|------|--------|------|
| FR-005 / FR-008 option-aware acceptance contract | Open | Downstream FRs still describe acceptance as selecting a quote, not an option and date. Deferred — FR-005's turn has not come. |
| `system-prd.md` FR-005 section | Open | One-quote-at-a-time acceptance wording predates the option model. Deferred with the item above. |
| `common_requirements` column | Open | Real spec-to-implementation gap; blocks REQ-004-020. |
| `graft_description_template` admin surface | Open | See note below. |
| System technical specification | Open | Not yet reconciled to the option aggregate. |

### Graft description trace (investigation, no change applied)

`graft_description` is generated **server-side** on both quote create and update from `AppSetting::get('graft_description_template', ...)`, seeded by `AppSettingsSeeder` as patient-facing text, and is persisted and delivered into the patient app's inquiry data model. However:

- **No app UI renders it** — the only app references are the model and entity files.
- **No admin surface edits the template** — no frontend reference to `graft_description_template` exists.
- **The provider form still submits it** — `CreateQuote.jsx` posts a `graft_description` value that the server unconditionally overwrites.

The PRD correctly marks the field system-generated and read-only. What is undocumented is where the template is owned and edited. Left as an open item pending a decision on template ownership.

---

## Files Changed

- `project-requirements/functional-requirements/fr004-quote-submission/prd.md` (v2.3 → v2.4)
- `project-requirements/functional-requirements/fr004-quote-submission/change-request-2026-09-09-quote-options-model.md`
- `project-requirements/system-data-schema.md`

No source code under `main/` was modified; it was read as reference only.
