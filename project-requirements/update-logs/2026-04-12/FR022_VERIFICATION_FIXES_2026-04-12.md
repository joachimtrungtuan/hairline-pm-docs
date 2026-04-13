# FR-022 Verification Fixes — 2026-04-12

**Type**: FR Verification Post-Fix  
**FRs Modified**: FR-022, FR-019, FR-011, FR-005  
**Date**: 2026-04-12  
**Trigger**: `/verify-fr FR-022` cross-FR search/filter consistency audit

---

## Summary

Following a full FR-022 verification pass focused on cross-FR search/filter consistency, 15 issues were identified and all resolved. Changes span FR-022 (primary), FR-019, FR-011, and FR-005.

---

## Changes Applied

### FR-022 — Search & Filtering (Primary)

#### Module Header & Scope
- **Issue 2**: Removed A-08 from module list and Multi-Tenant Architecture scope; added ~~A-08~~ strikethrough defer note in the admin modules list.

#### Master Reference Table
- **Issue 1**: Added `FR-019 / Screen 4` row (Admin / A-06 / Discount Code Catalog, Search ✓, Filter ✓, P1).
- **Issue 3**: Removed P-03 booking list row (no such patient-facing booking list exists per FR-006); removed REQ-022-047 and REQ-022-048 from Functional Requirements Summary; narrowed PR-01 module scope note.
- **Issue 4**: Added `FR-012 / Screen 2` row (Provider / PR-06 / Provider Messages Inbox, Search ✓, Filter ✓, P1).
- **Issue 13**: Added P-06, P-08, PR-01 to FR-022 module header and Multi-Tenant Architecture section.
- **Issue 15**: Renamed `FR-003 / Screen 11` heading from "Global Inquiry Table" to "Hairline Overview Dashboard" to match FR-003.

#### Screen Specifications — Provider Platform
- **Issue 5**: Changed FR-010/Screen 3 `Procedure Date Range` default from `All dates` to `Current month`.
- **Issue 6**: Removed `Clinician / Specialist` filter row from FR-011/Screen 8 (Aftercare Cases List); this field is absent from FR-011 and was not in client transcriptions.
- **Issue 7**: Removed Search View section from FR-016/Screen 7 (Admin Actions Audit Log) — search column was already `—` in the Master Reference Table; added `Show Only My Actions` toggle to the Filter View.
- **Issue 12**: Removed `role` from FR-009/Screen 10 search field (`Name / email / role / status` → `Name / email / status`); role is a Filter (handled by the Role Multi-select filter), not a search token per FR-009.
- **Issue 4 (spec)**: Added new `FR-012 / Screen 2: Provider Messages Inbox` screen spec under Module PR-06, with search (patient name / inquiry or quote ID / message content, 300ms, 2-char min) and 3 filters (Read Status, Date Range, Service Type).
- **Issue 1 (spec)**: Added new Module A-06 section with `FR-019 / Screen 4: Discount Code Catalog` screen spec (search: code/keyword, 500ms; filters: Status, Provider Participation, Date Range, Usage, ROI); marked as TODO placeholder pending FR-019 finalization.

#### Screen Specifications — Admin Platform
- **Issue 9**: Added Risk Level, Specialist Assignment, and Completion Rate filter rows to FR-011/Screen 13 (Admin Aftercare Cases List), aligning with FR-011 Screen 13 field additions.

#### Business Rules & Requirements
- **Issue 10**: Updated Rule 6 from `500ms` to `300–500ms depending on screen type — see REQ-022-012`; updated Admin Editability "Fixed in Codebase" debounce item to reference REQ-022-012 with both values.
- **Issue 11**: Changed Performance Rule 1 from `500ms` to `300ms`; changed REQ-022-005 from `500ms` to `300ms` (aligns with 300ms real-time filter target defined in REQ-022-012).
- **Issue 8**: Removed REQ-022-045 and REQ-022-046 (booking-list requirements with no backing screen).

---

### FR-019 — Promotions & Discount Management

- **Issue 1**: Added Screen 4 "Admin – Discount Code Catalog" as a TODO placeholder. Includes search (code/keyword) and 5 filters (Status, Provider Participation, Date Range, Usage, ROI). Change log updated to v1.2.
- Screen 4 cross-references FR-022 (`fr022-search-filtering/prd.md → screen code FR-019 / Screen 4`) with a note requiring simultaneous updates.

---

### FR-011 — Aftercare Recovery Management

- **Issue 9**: Added Risk Level, Specialist, and Completion Rate to Screen 13 (Admin Aftercare Cases List) `Search/Filters` field description. Change log updated to v1.3.

---

### FR-005 — Quote Comparison & Acceptance

- **Issue 14**: Updated Screen 1 `Sort & Filter` field description with explicit sort options (Price Low–High, Price High–Low, Graft Count, Rating, Quote Date), filter (patient-submitted date range), default sort (Quote Date most recent), and a cross-reference to `FR-022 / FR-005 / Screen 1`. Change log updated to v1.5.

---

## Files Changed

| File | Change |
|------|--------|
| `fr022-search-filtering/prd.md` | 13 targeted edits across module header, Master Reference Table, screen specs (Provider + Admin), Business Rules, Functional Requirements Summary |
| `fr019-promotions-discounts/prd.md` | Added Screen 4 placeholder (v1.1 → v1.2) |
| `fr011-aftercare-recovery-management/prd.md` | Extended Screen 13 search/filter field list (v1.2 → v1.3) |
| `fr005-quote-comparison-acceptance/prd.md` | Expanded Screen 1 Sort & Filter spec with canonical criteria + FR-022 cross-reference (v1.4 → v1.5) |
