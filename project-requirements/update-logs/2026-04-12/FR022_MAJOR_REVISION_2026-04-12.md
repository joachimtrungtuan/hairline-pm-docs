# FR-022 Major Revision — 2026-04-12

## Summary

Major revision of `local-docs/project-requirements/functional-requirements/fr022-search-filtering/prd.md` covering four areas: Mermaid workflow diagrams, screen code realignment, Master Reference Table corrections, and screen spec content updates from cross-FR audit.

---

## 1. Mermaid Workflow Diagrams

All flows in the **Business Workflows** section were converted from bullet-list steps to non-linear Mermaid flowcharts (`flowchart TD`). Each diagram uses decision diamonds, loop-back arrows, parallel entry points, and explicit reset paths.

**Flows converted:**

- **Main Flow 1** — Admin Patient Search & Filtering
- **Main Flow 2** — Admin Provider Search & Filtering
- **Main Flow 3** — Patient/Provider Self-Service Search & Filtering
- **Alternative Flow A1** — No Results Found (with search/filter refinement loop)
- **Alternative Flow A2** — Filter-Only Screens (no keyword search path)
- **Alternative Flow A3** — Bulk Action After Filtering
- **Alternative Flow A4** — Pagination After Filtering
- **Alternative Flow A5** — Autocomplete Suggestion Path
- **Alternative Flow A6** — Saved Filter Preset Application

**Key structural decisions:**
- Search and filter are co-equal, parallel entry points feeding into a single `QUERY` node — neither is subordinate to the other
- All "update keyword", "adjust filters", and "reset all" paths loop back explicitly to the shared control node
- Decision diamonds used for: "Records matched?", "Next action?", "Sufficient results?" branching

---

## 2. Screen Code Realignment (All Screen Specification Headings)

All screen specification headings were renamed from the invented module-based codes (e.g., `Screen P-02-001`, `Screen A-09-006`) to the canonical FR-based format used by each source FR.

**Format adopted:** `FR-XXX / Screen N` for screen-level entries; `FR-XXX / Screen N / Tab M` for tab-level entries within a screen.

**Full mapping applied:**

| Old Code | New Code | FR | Screen Name |
|----------|----------|----|-------------|
| P-02-001 | FR-003 / Screen 7a | FR-003 | Provider Selection |
| P-03-001 | ⚠ Gap (FR-006 pending) | FR-006 | Patient Bookings List |
| P-04-001 | FR-003 / Screen 8a | FR-003 | Booking Status Tracker |
| P-05-001 | FR-007 / Screen 1 | FR-007 | Patient Payment Progress |
| P-06-001 | FR-004 / Screen 4 | FR-004 | Treatment Plan List |
| P-07-001 | FR-010 / Screen 4 | FR-010 | Aftercare Day-by-Day List |
| P-08-001 | FR-011 / Screen 3 | FR-011 | Educational Resources Library |
| P-09-001 | FR-012 / Screen 1 | FR-012 | Messaging Inbox |
| P-10-001 | FR-025 / Screen 3 | FR-025 | Notification Center |
| PR-01-001 | FR-009 / Screen 1 | FR-009 | Patient Overview Table |
| PR-01-002 | ⚠ Gap (FR-009 pending) | FR-009 | Provider Activity Log |
| PR-01-003 | ⚠ Gap (FR-009 pending) | FR-009 | Work Queue |
| PR-02-001 | FR-003 / Screen 7b | FR-003 | Quote Request List |
| PR-03-001 | FR-006 / Screen 2 | FR-006 | Provider Booking List |
| PR-04-001 | FR-004 / Screen 3 | FR-004 | Provider Treatment Plan List |
| PR-05-001 | FR-014 / Screen 1 | FR-014 | Provider Analytics Dashboard |
| PR-06-001 | FR-024 / Screen 4 | FR-024 | Provider Package List |
| PR-06-002 | FR-032 / Screen 1 / Tab 5 | FR-032 | Reviews Tab |
| A-01-001 | FR-003 / Screen 11 | FR-003 | Global Inquiry Table |
| A-01-002 | FR-003 / Screen 8b | FR-003 | Inquiry Detail |
| A-01-003 | FR-006 / Screen 5 | FR-006 | Admin Bookings Table |
| A-02-001 | FR-007 / Screen 5 | FR-007 | Patient Payment Progress Dashboard |
| A-03-001 | FR-013 / Screen 4 | FR-013 | Admin Reviews Management |
| A-04-001 | FR-009 / Screen 10 | FR-009 | Team Directory |
| A-05-001 | FR-017 / Screen 7 / Tab 1 | FR-017 | Transaction Search |
| A-06-001 | FR-018 / Screen 1 | FR-018 | Affiliate Management |
| A-07-001 | FR-019 / Screen 2 | FR-019 | Discount & Voucher List |
| A-07-002 | FR-020 / Screen 3 | FR-020 | Referral Management |
| A-08-001 | ⚠ Gap (FR-021 pending) | FR-021 | Waiting List |
| A-09-001 | FR-026 / Screen 1 | FR-026 | App Data Management |
| A-09-002 | FR-027 / Screen 4A | FR-027 | User Acceptance List |
| A-09-003 | FR-029 / Screen 5 | FR-029 | Provider Commission Search |
| A-09-004 | FR-029 / Screen 6 | FR-029 | Currency Configuration |
| A-09-005 | FR-030 / Screen 1 | FR-030 | Notification Rules Dashboard |
| A-09-006 (old A-09-007) | FR-031 / Screen 1 / Tab 2 | FR-031 | Admin Users List |
| A-09-007 (old A-09-009) | FR-031 / Screen 1 / Tab 1 | FR-031 | Roles & Permissions |
| A-09-008 (old A-09-010) | FR-031 / Screen 5 | FR-031 | Admin Activity Audit Trail |
| A-09-009 (old A-09-011) | FR-033 / Screen 2 | FR-033 | FAQ Management |
| A-09-010 (old A-09-012) | FR-033 / Screen 3 | FR-033 | Article Management |
| A-09-011 (old A-09-013) | FR-033 / Screen 4 | FR-033 | Resource Management |
| A-09-012 (old A-09-014) | FR-033 / Screen 5 | FR-033 | Video Management |
| A-10-001 | FR-012 / Screen 5 | FR-012 | Communication Monitoring Center |
| A-10-002 | FR-034 / Screen 1 | FR-034 | Support Center Dashboard |

**Gap entries** (4 screens with no source FR screen yet defined):
- `⚠ Gap (FR-006 pending)` — Patient Bookings List (P-03)
- `⚠ Gap (FR-009 pending)` — Provider Activity Log (PR-01)
- `⚠ Gap (FR-009 pending)` — Work Queue (PR-01)
- `⚠ Gap (FR-021 pending)` — Waiting List (A-08)

---

## 3. Master Reference Table — Screen Code & Gap Fixes

The Master Reference Table's `Screen Code` column was corrected to use the same FR-based format. Gap rows and invalid entries were flagged or corrected.

**Changes:**
- All `P-XX-NNN` style codes replaced with `FR-XXX / Screen N` or `FR-XXX / Screen N / Tab M`
- Four screens marked `⚠ Gap` where no source FR screen exists yet
- Table is now the single source of truth for screen code → FR mapping

---

## 4. Screen Spec Content Updates — Cross-FR Audit Corrections

Eight screen spec entries were corrected after a parallel cross-FR audit comparing FR-022's filter/search criteria against the source FRs. All corrections align FR-022 with the source FR's actual implementation.

| Screen | Correction |
|--------|-----------|
| FR-014 / Screen 1 (Provider Analytics) | Added `Benchmarks Toggle` filter row (Show industry benchmarks overlay, default Off) |
| FR-032 / Screen 1 / Tab 5 (Reviews Tab) | Added `Sort` dropdown filter (Most recent, Highest rated, Lowest rated, Oldest first) |
| FR-009 / Screen 10 (Team Directory) | Added `Region` filter (Dropdown; admin-defined region list) |
| FR-006 / Screen 5 (Admin Bookings Table) | Added `Deposit Status` filter (Multi-select: Pending, Paid, Partial) |
| FR-027 / Screen 4A (User Acceptance List) | Added `Acceptance Timestamp` date range filter and `Reminder Status` multi-select filter |
| FR-031 / Screen 1 / Tab 2 (Admin Users List) | Fixed Status options: replaced `Pending Invitation` with `Pending Activation`; added `Inactive` |
| FR-031 / Screen 5 (Admin Activity Audit Trail) | Fixed Outcome options: replaced `Blocked` with `Denied` |
| FR-034 / Screen 1 (Support Center Dashboard) | Fixed Status options: replaced `Open, In Progress, Urgent, Unassigned` with `Open, In Progress, Closed, On Hold, Escalated` |

---

## 5. Gap Entry Removal

All 5 gap entries were removed from both the Master Reference Table and the detailed screen spec sections. These screens have no definition in their source FRs; rather than marking them as pending, they are treated as out of scope for FR-022 until the source FRs define them.

**Removed from Master Reference Table:**
- Patient / P-03 / FR-006 — Patient Bookings List
- Provider / PR-01 / FR-009 — Provider Activity Log
- Provider / PR-01 / FR-009 — Work Queue
- Admin / A-06 / FR-019 — Discount Code List
- Admin / A-08 / FR-014 — Analytics Reports Dashboard

**Removed from detailed spec sections:**
- `⚠ Gap (FR-006 pending): Patient Bookings List` — full spec block removed; Module P-03 section deleted
- `⚠ Gap (FR-009 pending): Provider Activity Log` — full spec block removed
- `⚠ Gap (FR-009 pending): Work Queue` — full spec block removed
- `⚠ Gap — Pending FR-019 Update` note — removed; Module A-06 section deleted
- `⚠ Gap (FR-014 pending): Analytics Reports Dashboard` — full spec block removed; Module A-08 section deleted

**Rationale:** FR-022 should only contain traceable entries pointing to screens that actually exist in source FRs. When FR-006, FR-009, FR-014, and FR-019 define these screens, FR-022 can be updated at that point.

---

## Files Modified

- `local-docs/project-requirements/functional-requirements/fr022-search-filtering/prd.md`
