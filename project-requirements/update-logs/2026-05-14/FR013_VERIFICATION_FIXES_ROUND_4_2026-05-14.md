# FR-013 Verification Fixes — Round 4

**Date**: 2026-05-14
**Files touched**:

- `local-docs/project-requirements/functional-requirements/fr013-reviews-ratings/prd.md` (→ v1.13)
- `local-docs/project-requirements/functional-requirements/fr020-notifications-alerts/prd.md` (→ v1.9)
- `local-docs/project-requirements/functional-requirements/fr030-notification-rules-config/prd.md` (→ v1.4)
- `local-docs/project-requirements/functional-requirements/fr022-search-filtering/prd.md`

**Trigger**: `/verify-fr FR-013` round 4 — 2 Critical, 4 Medium, 2 Minor issues raised; product owner selected resolution options inline (Issue #1 → Opt 1, #2 → Opt 1, #3 → confirm as owner requirement, #4 → Opt 1, #5 → Opt 1, #6 → Opt 1, #7 → Opt 1, #8 → Opt 1).

---

## Changes Applied

### 1. Issue #1 (Critical) — Audit-trail retention duration

**Constitution §VI requires 10-year audit-log retention**, but PRD previously stated only the 7-year review-content retention.

- Data & Privacy Rules now split the two retention windows explicitly:
  - Review content (review record + photos + provider responses + takedown requests) → **7 years minimum** (medical-records baseline, Constitution §III.A).
  - `AdminAction` / audit-log records (patient self-edits, admin edits/removals/seeded reviews, takedown decisions, settings changes, provider responses) → **immutable, 10 years minimum** (Constitution §VI).
- Screen 3 takedown retention notice rewritten to surface both windows so patients see the same split policy in the takedown confirmation modal.

### 2. Issue #2 (Critical) — Admin-seeded review provenance schema

Screen 8's "Source URL/evidence/date/permission note" pseudo-field replaced with a structured `source_metadata` form group:

- `source_platform` (enum: Google, Trustpilot, Doctolify, Provider Website, Email Testimonial, Other)
- `source_url` (URL; required unless platform = Email Testimonial)
- `evidence_file[]` (1–5 files; jpg/png/pdf; max 10MB each; stored via S-05)
- `capture_date` (ISO date; not future)
- `permission_record` (consent artifact: file or text reference) **+ admin attestation checkbox** confirming consent was obtained
- `reviewer_display_name` (admin-entered, PII-safe; carries the `Verified Off-platform` badge)

Key Entities Review extended with the matching `source_metadata` sub-structure (incl. `attested_by` / `attested_at`).

### 3. Issue #3 (Medium) — 3-month review eligibility gate

3-month post-procedure eligibility threshold confirmed by product owner as an **additional product requirement**, independent of any client-transcription source. No transcription evidence required. Threshold remains under "Fixed in Codebase" rules (`prd.md` § Business Rules / Admin Editability Rules). v1.13 Change Log entry records this confirmation as the authoritative source.

### 4. Issue #4 (Medium) — FR-014 per-treatment aggregation contract

Added **REQ-013-018a**: per-treatment aggregated sub-scores endpoint, providing `{treatment_id → {avg_overall, avg_facility, avg_staff, avg_results, avg_value, review_count, distribution}}` over Published reviews for a given provider. This is the explicit data contract consumed by FR-014's "review sub-scores per treatment" analytics. Cache invalidation triggered on publish, edit republish, removal, and approved takedown.

### 5. Issue #5 (Medium) — Patient self-edit safeguards

Main Flow Step 4 expanded to require on every patient edit/republish:

- Re-run B2 automated flagging (keyword/duplicate/rate-limit) on the new payload.
- Set `last_edited_at`, increment `edit_count`.
- Write full before/after audit record with `actor=patient`.
- Notify the provider that an existing review (possibly with their response) was edited, so they can re-evaluate.
- Surface an "Edited {relative_time}" marker on all public surfaces (Patient list, Patient detail, Provider list/detail, Provider Profile Reviews Section).

### 6. Issue #6 (Medium) — Reviewer alias algorithm

Canonical aliasing rule added to Data & Privacy Rules:

- Default: `{first_name} {last_initial}.` (e.g., "Sarah M.").
- Collisions within the same provider's review list deduplicate with numeric suffix (`Sarah M. 2`, `Sarah M. 3`, …).
- Admin views may unmask per RBAC.
- Admin-seeded reviews use admin-entered `reviewer_display_name` (PII-safe) instead of the algorithmic alias.
- V1 has no patient opt-in to expose full name; Screen 10 reviewer-display-policy toggle is reserved for future expansion and defaults to alias-only.

### 7. Issue #7 (Minor) — FR-022 master reference sync

`fr022-search-filtering/prd.md` updated:

- **FR-013 / Screen 7** filter row refreshed to current backend-aligned status vocabulary (`Published / Removed`; admin-internal `Flagged`) and expanded with Patient, Treatment Case, Source Type, and Response Status filters plus a Search field. Removed stale `Pending Moderation / Rejected` enums.
- **FR-013 / Screen 5** row added to the Provider Reviews List & Filters, including the patient filter introduced in FR-013 v1.7.
- Master-reference table at top of FR-022 updated with new FR-013/Screen 5 entry; FR-013/Screen 7 row marked as having both Search and Filter coverage.

### 8. Issue #8 (Minor) — Provider response "immutability" wording

Screen 6 business rule re-worded from "Provider responses are public and immutable once posted (admin can remove on violation)" to "immutable while published; admins may remove for policy violation; one replacement response allowed only after admin removal (per the one-active-response rule)" — eliminating the apparent contradiction with the existing replacement-after-removal allowance.

---

## Round 5 Follow-up — Selected Fixes

**Trigger**: `/verify-fr FR-013` follow-up — user selected Issue #1 → Option 1 and Issue #2 → Option 2.

### 9. Issue #1 (Critical) — Review notification catalog alignment

FR-013 requires invite/reminder, provider reply, admin removal, takedown decision, and provider new-review notifications through S-03. FR-020 already carried patient review status events, while FR-030 remained the source-of-truth notification catalog but only exposed `review.requested`.

- `fr030-notification-rules-config/prd.md` updated to v1.4 with Review event rows:
  - `review.requested` → Patient
  - `review.published` → Provider
  - `review.response_posted` → Patient
  - `review.removed_by_admin` → Patient
  - `review.takedown_decided` → Patient
- `fr020-notifications-alerts/prd.md` updated to v1.9:
  - Added provider-facing `review.published` event.
  - Aligned provider preference wording/entity to include `reviewNotification`, matching FR-032 Review Notifications.

### 10. Issue #2 (Medium) — Takedown reason required

User selected the stricter takedown model.

- FR-013 updated to v1.14:
  - Patient takedown workflow now requires a reason before submission.
  - Screen 3 field changed from optional `Takedown message` to required `Takedown reason` (10–1000 chars).
  - REQ-013-020 and `TakedownRequest` entity now require `reason`.
  - Remaining Screen 10 wording cleaned so review invite/reminder cadence stays owned by FR-030 link-outs, while FR-013 owns review labels, display policy, removal reasons, flagging/SLA settings, and exports.

### 11. Status closeout — PRD verified

FR-013 updated to v1.15 and marked `✅ Verified & Approved`.

- Header `Status` changed from `Draft` to `✅ Verified & Approved`.
- Appendix Change Log received a v1.15 status-closeout row.
- Appendix Approvals table aligned to `.specify/templates/prd-template.md` format and filled with `✅ Verified & Approved` status for Product Owner, Technical Lead, and Stakeholder rows dated 2026-05-14.

---

## Verification

- PRD now passes the FR-013 round-4 verification gate without remaining Critical or Medium issues.
- Constitution §II (Medical Data Privacy & Security) and §VI (Audit Trail) alignment restored.
- FR-014 integration contract is now explicit (REQ-013-018a).
- FR-022 master reference reflects current FR-013 filter surfaces.
- FR-030 and FR-020 review notification catalogs now both expose `review.published`, `review.response_posted`, `review.removed_by_admin`, and `review.takedown_decided`.
- FR-013 takedown flow no longer mixes optional `message` with required admin `reason`.
- FR-013 header status, Change Log, Approvals section, and Last Updated footer match PRD template closeout expectations.

---

## Cross-references

- `FR013_VERIFICATION_FIXES_2026-05-14.md` (rounds 1–3) — prior verification cycles
- `local-docs/project-requirements/functional-requirements/fr013-reviews-ratings/prd.md` (v1.13)
- `local-docs/project-requirements/functional-requirements/fr022-search-filtering/prd.md`
- Constitution §III.A (7-year medical records), §VI (10-year audit trail)
