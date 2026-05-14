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
