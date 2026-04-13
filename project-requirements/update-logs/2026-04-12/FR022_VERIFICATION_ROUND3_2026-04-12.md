# FR-022 Verification Round 3 Fixes

**Date**: 2026-04-12
**Type**: Major Update
**Document(s) Modified**: `local-docs/project-requirements/functional-requirements/fr022-search-filtering/prd.md`
**Version**: 2.2 → 2.3

---

## Summary

Third verification pass applying 8 issue resolutions from the FR-022 verification report. Changes cover PHI masking compliance, search algorithm standardization, filter logic disambiguation, max-length consistency, missing entry points, a missing debounce value, expanded dependency documentation, and a P2 spec gap marker for export functionality.

---

## Changes Applied

### 1. PHI Masking — Patient Name Excluded from Provider-Facing Search (Critical)

**Scope**: FR-003/Screen 9, FR-004/Screen 2, Privacy Rule 1, REQ-022-033, REQ-022-035, Module Scope PR-02

- FR-003/Screen 9 search field updated from `Patient ID / name` to `Patient ID` only; note added: "patient name excluded from search field until booking payment confirmed"
- FR-004/Screen 2 search field updated from `Patient / inquiry / …` to `Patient ID / inquiry / …`; same exclusion note added
- Privacy Rule 1 rewritten to mandate exclusion (not just anonymization), with explicit reference to the two affected screens
- REQ-022-033 updated to "patient ID only (patient name excluded … until booking payment confirmation)"
- REQ-022-035 updated to "patient ID, inquiry, treatment, date, status, and location fields (patient name excluded until booking payment confirmation)"
- Module Scope PR-02 bullet updated to note patient name exclusion pre-payment

---

### 2. Fuzzy Matching Standardization (Medium)

**Scope**: All screen spec search field Notes columns, Business Rule 2, REQ-022-007, Implementation Notes, External Dependencies

- All instances of "partial match" / "Partial match" globally replaced with "fuzzy match" / "Fuzzy match" across all screen specs
- Business Rule 2 example expanded: now includes accent-insensitive matching (José / Jose) alongside the substring example
- REQ-022-007 updated to "System MUST support case-insensitive fuzzy matching (via database full-text indexes)"
- Implementation Notes — Full-Text Search bullet updated from "Consider MySQL FULLTEXT…" to "Implement MySQL FULLTEXT or PostgreSQL TSVECTOR indexes — fuzzy matching via database full-text search is the MVP standard"
- External Dependencies — P3 Elasticsearch/Algolia note updated to clarify P3 scope is *advanced* fuzzy (synonym expansion, edit-distance) above and beyond MVP database fuzzy matching

---

### 3. Admin Search Query Max Length: 100 → 200 chars (Medium)

**Scope**: Business Rules — Admin Editability, Fixed in Codebase section

- Updated "Search query max length (100 chars for admin, 50 for patient)" to 200 chars for admin, aligning with FR-015/Screen 1 (200-char provider name search) and FR-032/Screen 5 (200-char Help Centre search)

---

### 4. Multi-Select Filter Logic Disambiguation (Medium)

**Scope**: All screen spec filter tables (Logic column), Control Behavior Standards

- All `| AND |` entries in screen spec filter Logic columns globally replaced with `| OR (within field) |`
- New **Filter Logic Note** added immediately after the Control Behavior Standards table: clarifies that AND applies *across* different active filter types, while OR applies *within* a single multi-select filter field

---

### 5. Internal Dependencies — Source FR Maintenance Table Added (Medium)

**Scope**: Dependencies section — Internal Dependencies subsection

- New maintenance dependency table added listing all 30+ source FRs and their owned screens, with explicit note: "Any screen-level change to a search field or filter criterion in a source FR must trigger an update to the FR-022 Master Reference Table"

---

### 6. Provider Platform Entry Points Added (Minor)

**Scope**: Module Scope — Entry Points section

- New **Provider Platform [P1 - MVP]** sub-section added with access paths for all six PR modules (PR-01 through PR-06), listing the specific screen code each entry point navigates to

---

### 7. Missing Debounce on FR-035/Screen 1 (Minor)

**Scope**: FR-035/Screen 1 (Help & Support Hub) search field table

- Debounce column updated from "—" to "300ms", consistent with other help content search screens and the Control Behavior Standards requirement

---

### 8. Export Functionality — P2 Spec Gap TODO Added (Minor)

**Scope**: Functional Requirements Summary — REQ-022-009

- TODO block added below REQ-022-009 marking export as a P2 spec gap: button placement, output columns, per-page behavior, and eligible screens are not yet defined; implementation is blocked until screen-level spec is written

---

## Verification Checklist

- [x] All PRD sections analyzed individually
- [x] Fresh searches performed per section
- [x] Screen field provenance checked for all UI sections
- [x] Dependency business rule conflicts checked
- [x] Dependency data field conflicts checked
- [x] All findings verified in post-check
- [x] Each issue has 3+ solution options
- [x] Report within word limit
- [x] No unsupported claims
