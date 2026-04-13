# FR-022 Verification Round 2 Fixes — 2026-04-12

**Type**: FR Verification Post-Fix
**FRs Modified**: FR-022 (`prd.md`), `system-prd.md`
**Date**: 2026-04-12
**Trigger**: `/verify-fr FR-022` — second verification pass; 10 issues identified, 8 resolved in this session

---

## Summary

Second verification pass on FR-022 (Search & Filtering) identified 6 medium and 4 minor issues. 8 issues were resolved in this session; Issue 6 (Transaction Search status enumeration) and Issue 7 (fuzzy matching terminology) were handled per user direction.

---

## Changes Applied

### Issue 1 — Treatment type filter removed (Option 2: remove from spec)

**Files**: `fr022-search-filtering/prd.md`

Removed "treatment type" from three locations where it was incorrectly specified but absent from the actual screen spec (FR-016/Screen 1) and source FR-016 PRD:

- Module Scope line (A-01 description): removed ", treatment type"
- Main Flow 1 FILTER node: removed ", treatment type" from filter label
- REQ-022-002: removed "and treatment type" from patient filter requirement

**Rationale**: Neither FR-022's screen spec for FR-016/Screen 1 nor the source FR-016 PRD include a Treatment Type filter. Retaining the requirement without a matching screen spec would make REQ-022-002 formally untestable.

---

### Issue 2 — Main Flow 2 workflow diagram corrected (Option 1: fix diagram)

**Files**: `fr022-search-filtering/prd.md`

Corrected two diagram nodes in Main Flow 2 (Admin Provider Search) to match FR-015/Screen 1 screen spec:

- KEYWORD node: was "clinic name, location, certification" → now "provider name, clinic name, email, license number"
- FILTER node: was "status, location, specialties, performance metrics" → now "status, featured, commission type, date range"

**Rationale**: Diagram previously described fields not present in the screen spec or FR-015 source, which would have caused dev/QA misalignment.

---

### Issues 3 & 4 — System PRD FR-022 module list corrected

**Files**: `system-prd.md`

Removed P-03 and A-08 from the FR-022 module list:

- P-03 (Patient Booking & Payment): Removed — patient booking list search/filter is deferred pending FR-006 update; no P-03 screen is defined in FR-022
- A-08 (Analytics & Reporting): Removed — no Admin Analytics FR exists; FR-022 correctly struck out A-08 scope

**Before**: `P-02, P-03, P-06, P-08 (Patient) | ... | A-01, A-02, A-03, A-05, A-06, A-07, A-08, A-09, A-10 (Admin)`
**After**: `P-02, P-06, P-08 (Patient) | ... | A-01, A-02, A-03, A-05, A-06, A-07, A-09, A-10 (Admin)`

---

### Issue 5 — User Story 2 / Scenario 2 rewritten (Option 1: rewrite scenario)

**Files**: `fr022-search-filtering/prd.md`

Replaced incorrect acceptance scenario that tested searching by location (not supported by screen spec) with a correct scenario testing the Location filter control:

- **Before**: "When they enter 'Istanbul' in the search field, Then the system returns all providers located in Istanbul"
- **After**: "When they select 'Turkey' from the Location filter, Then the system returns only providers whose location matches Turkey"

---

### Issue 6 — Transaction Search status filter enumerated (Option 1: enumerate inline)

**Files**: `fr022-search-filtering/prd.md`

Replaced the vague placeholder "All applicable statuses per record type" with a full inline enumeration table showing status options per Record Type:

| Record Type | Status Options |
|---|---|
| Invoice | Pending, Partial, Paid, Overdue, Refunded, At Risk |
| Provider Payout | Pending, Approved, Paid, Voided, Failed |
| Installment | Active, Completed, Overdue, Defaulted |
| Refund | Processing, Completed, Failed |
| Affiliate Commission | Pending, Paid, Failed, Cancelled |

Also documented union behavior: when multiple record types are selected, the union of all applicable statuses is shown.

---

### Issue 9 — Footer "Last Updated" date corrected

**Files**: `fr022-search-filtering/prd.md`

Updated footer date from `2026-04-03` to `2026-04-12` to match the Change Log v2.1 entry.

---

### Issue 10 — Approvals table updated

**Files**: `fr022-search-filtering/prd.md`

Replaced all `[Status]` placeholders with `Pending` and `[Date]` with `2026-04-12` across all three approval rows (Product Owner, Technical Lead, Stakeholder). Names left as `[Name]` pending stakeholder assignment.

---

## Issues Not Modified

| Issue | Decision |
|---|---|
| Issue 7: "Fuzzy matching" terminology | Leave as-is (Option 3) — acceptable approximation for diagrams/notes |
| Issue 8: Broken "see deferred items below" reference | Leave as-is — linked to Issue 3 root cause; deferred items section creation deferred |
