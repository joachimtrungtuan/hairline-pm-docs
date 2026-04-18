# FR-014 Verification Fixes (Round 2)

**Date**: 2026-04-17
**Report Type**: FR-014 verification and correction (v3.3)
**Primary Document**: `local-docs/project-requirements/functional-requirements/fr014-provider-analytics-reporting/prd.md`
**Related Schema**: `local-docs/project-requirements/system-data-schema.md`

---

## Summary

Second round of verification fixes for FR-014 (Provider Analytics & Reporting), addressing issues found during structured `verify-fr` audit. All changes are backed by backend migration review.

---

## Changes Applied

### 1. Issue #1 — Last-Activity Source Resolved (Critical)

**Problem**: PRD referenced `provider_users.last_login_at` which does not exist in the database schema or any migration.

**Backend finding**: `provider_users` table has no login timestamp column (confirmed across all 9 provider_users migrations). The `provider_activity_logs` table (created 2025-12-09) is the canonical activity log — it records `action_type` (including `login`) and `action_at` per provider user.

**Changes**:
- Updated Screen 8 Widget 3 "Last active" column source to `MAX(provider_activity_logs.action_at)` per provider
- Updated Screen 8 Business Rules to reference `provider_activity_logs` as the canonical source
- Updated Dependencies section — removed `provider_users.last_login_at` reference, added `provider_activity_logs` with correct query pattern
- Updated Entity 5 — replaced ambiguous `last_login_at` field with `last_active_at` and `last_login_at` (both sourced from `provider_activity_logs`)
- Added `provider_activity_logs` table definition to `system-data-schema.md` (was missing)

---

### 2. Issue #2 — Commission Formula Corrected (Critical)

**Problem**: Business Rules "Fixed in Codebase" stated `payment.amount × quote.commission / 100`, which is percentage-only. Multiple screen specs (Screens 4, 7, 12) and REQ-014-051 require support for both `percentage` and `flat rate` commission models.

**Change**: Replaced the formula with conditional logic:
> `IF provider_commissions.type = 'percentage' THEN payment.amount × (effective_rate / 100) ELSE effective_flat_amount`

The conditional structure is fixed; the rate/amount values are sourced from provider commission configuration.

---

### 3. Issue #3 — SLA Scope Clarified (Critical)

**Problem**: SLA target listed as "per provider" (admin-configurable) but no `sla_target` field exists anywhere in the schema. Assumption 4 acknowledged the gap as unresolved.

**Resolution**: Scoped SLA to a single platform-wide configurable value (in minutes). Per-provider SLA overrides deferred to a future version.

**Rationale for minutes**: Backend TTFQ test data shows response times from 30 min to 6+ hours. Days would be too coarse for meaningful SLA differentiation.

**Changes**:
- Assumption 4 updated to reflect platform-wide SLA with rationale
- Admin Editability rule updated (removed "per provider", added scope note)
- Screen 7 Business Rules updated (removed reference to individual provider SLA)

---

### 4. Issue #4 — Screen 7 B2 Drill-Down Fixed (Medium)

**Problem**: Screen 7, Section B2 (Platform TTFQ Distribution) drill-down linked back to Screen 7 itself.

**Change**: Corrected target to "Screen 8 (Provider Performance & Engagement) sorted by TTFQ".

---

### 5. Issue #5 — Module Scope Screen Count Corrected (Medium)

**Problem**: Module Scope stated "5-screen analytics suite" for Provider Platform (PR-05), but Executive Summary and System PRD both say 6 provider screens.

**Change**: Updated to "6-screen suite (5 screens in the 'Analytics' nav + Screen 1 as the platform landing page)" with the distinction made explicit. Business Workflow outcome also updated from "5 analytical screens" to "6 provider screens".

---

### 6. Issue #6 — Admin Workflow Extended to All 7 Admin Screens (Medium)

**Problem**: Admin main workflow stepped through Screens 7 → 8 → 9 → 10 → 12, skipping Treatment Outcomes (Screen 11) and Pricing Intelligence (Screen 13) with no documented entry path.

**Change**: Added Steps 5 and 7 to the admin workflow — Screen 11 (Treatment Outcomes) and Screen 13 (Pricing Intelligence) — making the workflow cover all 7 admin screens.

---

### 7. Issue #7 — Screen 6 Export Exclusion Documented (Minor)

**Problem**: Screen 1 (Main Dashboard) was silently excluded from Screen 6 export options with no explanation.

**Change**: Added inline note to the "Screens to include" field: "Screen 1 is excluded — it contains real-time operational data not suitable for static reports."

---

### 8. Issue #8 — REQ Numbering Resequenced (Minor)

**Problem**: Screen 6 requirements were numbered REQ-014-101 to REQ-014-104 (out of sequence), while Screens 7–13 used REQ-014-060 to REQ-014-100. This created a gap and confusion.

**Change**: Screen 6 reassigned to REQ-014-060 through REQ-014-063. Screens 7–13 shifted up by 4 (REQ-014-064 through REQ-014-104). Final sequence: REQ-014-001 to REQ-014-104, continuous and gap-free.

| Screen | Old Range | New Range |
|--------|-----------|-----------|
| Screen 6 | REQ-014-101–104 | REQ-014-060–063 |
| Screen 7 | REQ-014-060–064 | REQ-014-064–068 |
| Screen 8 | REQ-014-065–069 | REQ-014-069–073 |
| Screen 9 | REQ-014-070–075 | REQ-014-074–079 |
| Screen 10 | REQ-014-076–080 | REQ-014-080–084 |
| Screen 11 | REQ-014-081–086 | REQ-014-085–090 |
| Screen 12 | REQ-014-087–094 | REQ-014-091–098 |
| Screen 13 | REQ-014-095–100 | REQ-014-099–104 |

---

## Minor Follow-Up Note

- Clarified that FR-014 consumes the existing permission model rather than defining new roles, changed the provider workflow actor wording to "Provider user with analytics access", added an explicit rule that unauthorized widgets are not rendered or queried, and added FR-026 / FR-031 to Dependencies as the settings and access-control sources for analytics behavior.
