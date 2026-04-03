---
date: 2026-04-03
type: major
fr: FR-022
title: FR-022 Screen Specifications Overhaul — Three-Tenant Structure, Master Reference Table, Provider Platform Expansion
---

# FR-022 Screen Specifications Overhaul

**Date**: 2026-04-03  
**Type**: Major Update  
**Affected Files**:
- `local-docs/project-requirements/functional-requirements/fr022-search-filtering/prd.md`
- `local-docs/project-requirements/system-prd.md`

---

## Summary

FR-022 underwent a comprehensive overhaul of its Screen Specifications section. The previous version contained only 4 screens (2 Admin + 2 Patient P2) and was missing the entire Provider Platform. This update brings FR-022 to its intended scope as the platform-wide single source of truth for all search and filter criteria.

---

## Changes Made

### FR-022 — Screen Specifications (Major Rewrite)

**Before**: 4 screens in a flat list (Screen 1–4), no behavioral states, no Provider Platform coverage, no master reference table.

**After**:

1. **Maintenance Convention note** added at the top of the section — establishes the living-document protocol: any source FR that changes its filter/search field list must trigger an update to FR-022's Master Reference Table.

2. **Master Reference Table** added — 54 rows covering all screens across all three tenants, organized by Tenant → Module → FR → Screen Name with screen codes (e.g., `A-01-007`), search/filter capability flags, and priority.

3. **Three-tenant structure** introduced:
   - **Patient Platform** (6 screens): P-02 Provider Selection, P-02 Quote Comparison, P-03 Bookings, P-06 Messages Inbox, P-08 Help Center, P-08 Support Tickets
   - **Provider Platform** (11 screens, new): PR-01 Team Directory, PR-01 Activity Log, PR-01 Work Queue, PR-02 Inquiry List, PR-02 Quote List, PR-03 In Progress Cases, PR-04 Aftercare Cases, PR-05 Analytics Dashboard, PR-06 Package List, PR-06 Reviews Tab, PR-06 Support Cases
   - **Admin Platform** (37 screens): All A-01 through A-10 modules fully specified

4. **Screen format** — each screen has:
   - Two sub-sections: **Search View** (search fields table) and **Filter View** (filter controls table), as distinct specs
   - **Control behaviors mini-table** in each view: states = Search Inactive, Search Active (for search views) / Filter Inactive, Filter Active, Reset Filter (for filter views)

5. **A-06 Gap documented**: FR-019 does not currently define a Discount Code List screen. Gap is noted with a placeholder and instructions for when FR-019 is updated.

### FR-022 — Other Sections Updated

- **Executive Summary**: Updated to reflect all three tenants as co-equal; Provider Platform now listed as P1-MVP alongside Admin; maintenance convention cross-referenced
- **Module Scope / Multi-Tenant Architecture**: Updated to include PR-01 and Patient P1 screens; detailed breakdown revised
- **Functional Requirements Summary**: Added new REQ entries (REQ-022-033 through REQ-022-056) for Provider Platform screens and Patient P1 screens; grouped existing Admin reqs; added shared behavior rules
- **Change Log**: Version 2.0 entry added

### System PRD Updates

- **FR-022 section** (line ~1170): Priority corrected from P2 to P1 (MVP) for Provider/Admin; requirement bullets replaced with pointer to FR-022 as the single source of truth; maintenance convention added
- **Line ~441** (inquiry submission): Added `(see FR-022 Screen P-02-001)` pointer
- **Line ~518** (quote comparison): Added `(see FR-022 Screen P-02-002)` pointer
- **Line ~1045** (admin patient mgmt): Added `(see FR-022 Screen A-01-007)` pointer
- **Line ~1678** (activity log): Added `(see FR-022 Screen A-09-010)` pointer

---

## Screens Inventory (Summary)

| Tenant | Module Count | Screen Count |
|--------|-------------|-------------|
| Patient | 4 modules (P-02, P-03, P-06, P-08) | 6 screens |
| Provider | 6 modules (PR-01 through PR-06) | 11 screens |
| Admin | 10 modules (A-01 through A-10) | 37 screens |
| **Total** | | **54 screens** |

Note: 1 gap (A-06-001) pending FR-019 update.

---

## Subsequent Refinement (same date)

- **Control Behavior Standards section added**: All per-screen behavior state tables (Search Inactive / Search Active / Filter Inactive / Filter Active / Reset Filter) were extracted into a single shared `### Control Behavior Standards` section placed before the tenant screen listings. Each screen now carries a one-line pointer to this section instead of repeating the table. File reduced from ~2447 to ~2071 lines.

---

## Maintenance Reminder

When any of the following FRs update their filter or search field lists, update FR-022 accordingly:

FR-003, FR-004, FR-005, FR-006, FR-007, FR-007b, FR-009, FR-010, FR-011, FR-012, FR-013, FR-014, FR-015, FR-016, FR-017, FR-018, FR-019, FR-024, FR-025, FR-027, FR-029, FR-030, FR-031, FR-032, FR-033, FR-034, FR-035
