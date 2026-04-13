# FR-022 Verification Round 4 Fixes — 2026-04-13

**FR**: FR-022 Search & Filtering
**PRD Version**: 2.3 → 2.4
**Type**: Post-verification issue resolution (Medium × 5, Minor × 2)

---

## Summary

Seven issues identified during verification round 4 were resolved by applying user-selected resolution options. Changes span FR-022 (`fr022-search-filtering/prd.md`) and the system PRD (`system-prd.md`).

---

## Changes Applied

### Medium Issue #1 — Specialist Filter Removed from Provider Aftercare Scope (Option 2)

**Root cause**: Module Scope (L51) and REQ-022-039 listed "specialist" as a provider-facing filter for FR-011/Screen 8, but the screen spec did not include it and the source FR-011 PRD confirmed no specialist filter exists at the provider level. Specialist filtering is an admin-only capability (A-03).

**Changes to FR-022 PRD**:
- Module Scope PR-04: removed "specialist" from filter list → now reads "filter by milestone, status, and date"
- REQ-022-039: removed "specialist" → now reads "search and filter aftercare cases by patient name/ID, milestone, status, and date range"

---

### Medium Issue #2 — B2 Overflow Workflow Removed; Pagination is Authoritative (Option 1)

**Root cause**: B2 workflow described a hard 100-result truncation model ("System shows first 100 results with overflow warning message"). This directly contradicted REQ-022-006 ("paginate search results, default 25 results per page"), Business Rule 3, and Performance Rule 3, all of which mandate proper pagination.

**Changes to FR-022 PRD**:
- Removed the entire B2 "Search returns too many results (>100)" alternative flow section and its Mermaid diagram
- Renumbered former B3 (database unavailability) to B2
- Edge Case 2: updated handling from "Return first 100 matches" to paginated first-page display (25/page per REQ-022-006) with an informational filter guidance banner

**Side effect**: Minor Issue #2 (undefined interaction between configurable page size and overflow threshold) resolved automatically by this removal — the overflow concept no longer exists.

---

### Medium Issue #3 — REQ-022-009 Export Moved to P2 (Option 1)

**Root cause**: REQ-022-009 was placed under the "Core Requirements (P1 - MVP)" heading but had an inline note explicitly marking it as P2 pending spec completion. Ambiguous placement risked development teams scheduling incomplete export work in the MVP sprint.

**Changes to FR-022 PRD**:
- Removed REQ-022-009 (and its TODO note) from the Core Requirements (P1) Admin Platform section
- Added REQ-022-009 to the Enhanced Requirements (P2) section with a consolidated inline note explaining the spec gap

---

### Medium Issue #4 — System PRD Screen Code Cross-References Updated (Option 1)

**Root cause**: System PRD referenced FR-022 screens using an old internal code format (P-02-001, P-02-002, A-01-007, A-09-010) that no longer exists in FR-022, which adopted source-FR-based screen codes in v2.0.

**Changes to system-prd.md**:

| Location | Old reference | New reference |
|----------|--------------|---------------|
| L441 (FR-003 provider filter) | `FR-022 Screen P-02-001` | `FR-022 / FR-003 / Screen 7a` |
| L518 (FR-005 quote comparison filter) | `FR-022 Screen P-02-002` | `FR-022 / FR-005 / Screen 1` |
| L1045 (FR-016 patient search) | `FR-022 Screen A-01-007` | `FR-022 / FR-016 / Screen 1` |
| L1678 (FR-031 activity audit trail filter) | `FR-022 Screen A-09-010` | `FR-022 / FR-031 / Screen 5` |

---

### Medium Issue #5 — Active Status and Available Capacity Filters Added to FR-003/Screen 7a (Option 1)

**Root cause**: System PRD (L441) requires patient-facing provider search to filter by "active status" and "available capacity", but FR-022/Screen 7a (FR-003/Screen 7a, P2) only specified Country/Destination, Rating, and Specialty filters.

**Changes to FR-022 PRD**:
- Added two filter rows to FR-003/Screen 7a Filter View table:
  - `Active Status` — Segmented (All / Active Only), default Active Only
  - `Available Capacity` — Toggle (Show providers with open appointment slots only), default Off

---

### Minor Issue #1 — Implementation Notes Debounce Corrected (Option 1)

**Root cause**: Implementation Notes stated a blanket "500ms" debounce, contradicting per-screen specs that use 300ms (FR-012, FR-024, FR-031, FR-035) and REQ-022-012 which specifies "300–500ms depending on screen type."

**Changes to FR-022 PRD**:
- Debouncing note updated to: "Implement client-side debounce (300–500ms per screen type, per REQ-022-012)"

---

## Files Modified

| File | Change type |
|------|------------|
| `local-docs/project-requirements/functional-requirements/fr022-search-filtering/prd.md` | Multiple targeted edits (v2.3 → v2.4) |
| `local-docs/project-requirements/system-prd.md` | 4 cross-reference updates |
