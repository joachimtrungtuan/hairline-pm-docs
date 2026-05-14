# FR-013 Verification Fixes — 2026-05-14

**Type**: Multi-document alignment following FR-013 verification  
**Scope**: FR-013, FR-032, FR-020, FR-022, system-prd.md  
**Triggered by**: FR-013 verify-fr run — 8 confirmed issues, all resolved with solution option 1

---

## Changes Applied

### FR-013 (fr013-reviews-ratings/prd.md) — v1.11

**Issue #4 — B2 Flagging Workflow:**
- Narrowed B2 trigger to system-automated detection only (keyword matching, duplicate patterns, rate limits)
- Removed "flagged by users" — user-initiated flagging moved to future enhancement
- No corresponding screen specification existed for user-facing flag actions

**Issue #6 — Feedback Minimum Length:**
- Added rationale to Screen 1 feedback field validation note: 100-char minimum ensures reviews contain enough substance to be useful to other patients

**Issue #7 — Metrics Recalculation in A4:**
- Updated A4 step 3 to explicitly include provider rating metrics recalculation when a takedown is approved
- Aligns A4 main workflow with existing edge case documentation

**Issue #8 — SC-005 Reclassification:**
- SC-005 ("80% of published reviews receive a provider response within 5 business days") reclassified as a Business KPI
- Annotated as tracked via FR-014 analytics, not enforced by FR-013 system behavior

---

### FR-032 (fr032-provider-dashboard-settings/prd.md) — v1.5

**Issue #1 — Provider Response Scope Conflict:**
- Removed "read-only / future enhancement" designation for provider responses in Reviews tab
- Updated 6 locations: module scope bullet, Tab 5 Purpose, Tab 5 Business Rules (2 rules), General Business Rule 5, Entity 7 name/description
- Tab 5 is now designated "Read/Respond": review content remains read-only, response composer is in scope per FR-013 Screen 6

---

### FR-020 (fr020-notifications-alerts/prd.md) — v1.8

**Issue #2 — Missing Notification Events:**
- Added three missing review notification events to the event catalog:
  - `review.response_posted` — patient notified when provider posts public response
  - `review.removed_by_admin` — patient notified when admin removes their review
  - `review.takedown_decided` — patient notified of takedown approve/reject decision
- Required by FR-013 REQ-013-016

---

### FR-022 (fr022-search-filtering/prd.md) — v2.10

**Issue #3 — Stale Screen Reference:**
- Updated all three occurrences of `FR-013 / Screen 2 (Review Management Dashboard)` → `FR-013 / Screen 7`
- FR-013 v1.8 renumbered this screen; FR-022 had not been updated

---

### system-prd.md

**Issue #5 — Patient Review Edit Not in System PRD:**
- Added explicit requirement: "Patients MUST be able to edit their published review at any time"
- Aligns system PRD with FR-013 Screen 1/3 and REQ-013-018, which were already in scope since v1.2

---

## Round 2 — Second verify-fr Pass (same date)

**Triggered by**: Follow-up `/verify-fr FR-013` run after Round 1 fixes — 5 new confirmed issues (0 critical, 3 medium, 2 minor), all resolved with solution option 1.

### FR-013 (fr013-reviews-ratings/prd.md)

**Issue #1 — FR-014 missing from Dependencies:**
- Added FR-014 (Provider Analytics & Reporting) to Internal Dependencies with a one-line note describing the ratings/sub-scores/aggregate-trends feed
- Closes traceability gap with system PRD FR-014 which explicitly consumes review sub-scores per treatment and rating trends

**Issue #2 — Recalculation on patient edit not specified:**
- Extended Main Flow Step 3 to state recalculation (average, count, distribution) and cache invalidation occur on both initial publish and edit-republish paths
- Removes ambiguity that could leave provider averages stale after edits

**Issue #3 — Patient self-edit audit trail not explicit:**
- Broadened the Data & Privacy audit rule to cover all review mutations (patient self-edits, admin actions, provider responses) with actor type and before/after capture
- Closes constitution VI (Auditability) gap

**Issue #4 — Length bounds lack provenance:**
- Added Notes-line rationale to Screen 1 (feedback 100–2000 chars) and Screen 6 (provider response 50–1000 chars) citing UX, anti-spam, and scannability reasoning
- Bounds remain "Fixed in Codebase" per existing Business Rule

### system-prd.md

**Issue #5 — "One review per completed procedure" not in system PRD:**
- Added explicit requirement to FR-013 mandating uniqueness keyed to patient + completed procedure record, with the edit flow operating on the existing review rather than creating new ones
- Aligns system PRD with FR-013 PRD L171/L480 which had previously enforced this without source backing

---

## Round 3 — Third verify-fr Pass (same date)

**Triggered by**: Follow-up `/verify-fr FR-013` run after Round 2 fixes — 5 new confirmed issues (0 critical, 2 medium, 3 minor). User selected solutions per issue.

### FR-013 (fr013-reviews-ratings/prd.md) — v1.12

**Issue #1 — FR-013 ↔ FR-030 cadence ownership overlap (Medium → Option 2):**
- Screen 10 "Invitation cadence" and "Reminder settings" rewritten as read-only link-outs to FR-030 (Notification Rules & Configuration), which owns the `review.requested` event timing/cadence
- REQ-013-022 updated to scope Screen 10 to category labels, photo guidelines, removal reasons, display policy, flagging/SLA, and exports — and to explicitly defer invite/reminder cadence to FR-030
- Eliminates dual source of truth for review-invite scheduling

**Issue #2 — Provider response lifecycle after admin removal (Medium → Option 1):**
- Screen 6 Business Rules updated: if admin removes a prior provider response for policy violation, provider may submit one replacement response
- Both removed and replacement responses retained in audit trail (`AdminAction` for removal, `ProviderResponse` history for lifecycle)
- Preserves provider voice while keeping the "at most one active response" rule

**Issue #3 — REQ-013-021 ordering anomaly (Minor → Option a):**
- Renumbered REQ-013-021 to REQ-013-009 so Core Requirements run sequentially 001–009
- Subsequent IDs in Data/Security/Integration sections shifted by one (former 009→010, 010→011, …, 020→021); REQ-013-022 retained as the final integration requirement

**Issue #4 — Photo guidelines "versioned" ambiguity (Minor → Option c):**
- Screen 10 photo guidelines validation note changed from "Required; versioned" to "Required; audit-logged (all edits captured via AdminAction with before/after values; no formal version model)"
- Clarifies intent matches existing audit-trail rule; no new schema fields needed on ReviewSettings

**Issue #5 — Takedown message minimum length (Minor → Option b):**
- Screen 3 takedown message validation updated: when provided, enforced minimum length of 10 chars
- Field remains optional; prevents trivial single-character submissions while keeping the no-context-required affordance
