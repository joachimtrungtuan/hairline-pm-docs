---
date: 2026-03-28
type: major
fr: FR-026, FR-001
module: A-09 System Settings & Configuration, P-01 Auth & Profile Management
author: AI
---

# FR-026 / FR-001 — Account Deletion Reasons Admin Management — 2026-03-28

## Summary

Added "Account Deletion Reasons" as a new centrally managed App Data list in FR-026 (App Settings & Security Policies), mirroring the existing "Inquiry Cancellation Reasons" pattern. FR-001 Screen 16 (Delete Account / DSR) previously referenced a hardcoded or unspecified deletion reason dropdown; that dropdown is now formally owned and seeded by FR-026.

---

## Changes Applied

### 1. FR-026 prd.md (v1.2 → v1.3)

#### Multi-Tenant Scope

- **Multi-Tenant Architecture P-01 line**: Added `account deletion reason options` to the list of items consumed by the Patient Platform.

#### Entry Points

- **Admin-Initiated entry point**: Updated navigation description to include `account deletion reasons` alongside existing App Data items.

#### Business Workflows

- **Alternative Flow A5 — Admin Edits Account Deletion Reasons**: New flow added after A4, documenting the trigger, 9-step admin interaction, and outcome. Mirrors A4 (Inquiry Cancellation Reasons) in structure.

#### Screen Specifications

- **Setting Groups (Screen 1)**: Added `Account Deletion Reasons (reason label, requires_explanation, display order, active)` under App Data.
- **Screen 5b — Account Deletion Reasons Manager**: New screen added after Screen 5a. Includes:
  - 4-column data fields table (Reason Label, Requires Explanation, Display Order, Active)
  - Business rules (uniqueness, min 2 active, "Others" FIXED, soft delete, 1-minute propagation, drag-drop reorder)
  - Notes (drag-drop UI, usage analytics, deactivation warning, change reason modal)
  - Consumer note: FR-001 Screen 16

#### Business Rules

- **Admin Editability Rules**: Added `Account deletion reasons: add, edit, reorder, deactivate reason options (FR-001 Screen 16 consumer)`
- **Configurable with Restrictions**: Added `Admin can deactivate account deletion reasons but must maintain at least 2 active reasons; "Others" reason cannot be deactivated`

#### Initial Configuration / Seeding

- **Account Deletion Reasons** — 9 initial options seeded:

| Order | Label | Requires Explanation |
|-------|-------|----------------------|
| 1 | I no longer use this app | No |
| 2 | I found a better alternative | No |
| 3 | The app doesn't meet my needs | No |
| 4 | Too many notifications or emails | No |
| 5 | Concerns about privacy or data security | No |
| 6 | I had technical issues or bugs | No |
| 7 | The app is difficult to use | No |
| 8 | I'm taking a break and may return later | No |
| 9 | Others | Yes (FIXED — cannot be deactivated) |

#### Edge Cases

- Added: "What happens when admin attempts to deactivate the 'Others' deletion reason?" — System prevents deactivation and displays error: `"Others" is a fixed reason and cannot be deactivated.`

#### Functional Requirements Summary

- **REQ-026-012b** (new): System MUST store centrally managed account deletion reason options: reason label, requires_explanation flag, display order, active status. Consumer: FR-001 Screen 16.

#### Key Entities

- **Entity 7 — Account Deletion Reason** (new): Centrally managed deletion reason option for FR-001 Screen 16. Key attributes: reason_id, reason_label, requires_explanation (boolean), display_order, active, usage_count, created_at, updated_at.
- **Entity 7 — Email Template** renumbered to **Entity 8** (no content change).

---

### 2. FR-001 prd.md

- **Screen 16 Data Fields — Reason for Deletion**: Validation Rules column updated to reference FR-026:
  - Old: `Optional; does not block submission; deleteAccountRequest { reason? }`
  - New: `Optional; does not block submission; deleteAccountRequest { reason? }; options centrally managed in Admin Settings (FR-026, App Data → Account Deletion Reasons)`
- **Dependencies — FR-026 entry**: Expanded to include deletion reason options:
  - Old: `App Settings & Security Policies (OTP + throttling config; centrally managed lists)`
  - New: `App Settings & Security Policies (OTP + throttling config; centrally managed lists including account deletion reason options for Screen 16)`

---

### 3. reports/2026-02-05/missing-mobile-flows-design-complement.md

- **Screen P01.1-S1 — Deletion Reason Selector row**: Updated Validation Rules from generic `"options are centrally managed (not hardcoded in this spec)"` to specific `"options centrally managed in Admin Settings (FR-026, App Data → Account Deletion Reasons)"`.

---

## Not Affected

- FR-003 Inquiry Cancellation Reasons (Screen 5a, Entity 6, REQ-026-012a) — unchanged.
- All other FRs — no screen numbering or dependency impact.
- FR-023 Data Retention & Compliance — still owns DSR lifecycle; FR-026 owns only the reason option list.
