---
date: 2026-03-28
fr: FR-026
type: verification-fixes
version: 1.3 → 1.4
---

# FR-026 Verification Fixes — 2026-03-28

**PRD**: `local-docs/project-requirements/functional-requirements/fr026-app-settings-security/prd.md`
**Version bump**: 1.3 → 1.4

## Summary

Applied 8 targeted fixes identified during FR-026 verification pass. All changes are corrections to existing content; no new features or screens added.

---

## Changes Applied

### Issue 1 — MFA Duplicate Bullet Removed (Implementation Notes)

- **Section**: Implementation Notes → Security Considerations
- **Change**: Removed duplicate `Authentication: Multi-factor authentication required` bullet
- **Reason**: REQ-026-017 already correctly scopes MFA as non-MVP, deferred to FR-031. The Implementation Notes bullet contradicted REQ-026-017 and would have caused implementation confusion.

### Issue 2 — Country Flag Added to Entity 4 and REQ-026-011

- **Sections**: Key Entities (Entity 4), Functional Requirements Summary (REQ-026-011)
- **Change**: Added `flag_url (text, nullable — URL to S-05-stored flag asset)` to Entity 4 key attributes; extended REQ-026-011 to include "country flag asset URL (stored via S-05 Media Storage, nullable)"
- **Reason**: Screen 4 and User Story 3 both require a country flag field (mandatory, stored via S-05), but the field was absent from the entity schema and functional requirement, which would have caused the backend to omit it from the database schema and API contract.

### Issue 3 — IP/Device-Level Rate Limiting Documented as Fixed-in-Codebase

- **Sections**: Business Rules → Fixed in Codebase, Implementation Notes → Security Considerations
- **Change**: Added IP/device-level rate limiting entry to Fixed in Codebase (max 20 failed login attempts per IP/hour, 1-hour lockout) and a Security Considerations bullet explaining the enforcement behaviour and its interaction with per-user throttling
- **Reason**: System PRD (line 1339) requires IP/device-level rate limiting for anti-brute-force protection. The FR-026 PRD had no coverage for this requirement.

### Issue 4 — Stale "FR-003 Screen 11" References Corrected to "Screen 8a"

- **Sections**: Screen 5a, Business Rules, REQ-026-012a, Dependencies, Edge Cases, Seeding notes (6 occurrences)
- **Change**: Global replace `FR-003 Screen 11` → `FR-003 Screen 8a`
- **Reason**: FR-003 v1.6 (2026-02-10) renumbered the Cancel Inquiry Confirmation Modal from Screen 11 to Screen 8a. In FR-003 today, Screen 11 is the Admin Hairline Overview Dashboard — a completely different screen.

### Issue 5 — Propagation Test Scenarios Updated from "30 seconds" to "1 minute"

- **Section**: User Scenarios & Testing (User Stories 1–5, acceptance scenario 3/4)
- **Change**: Changed `30 seconds ago` → `at least 1 minute ago` in the 4 propagation acceptance scenarios
- **Reason**: The propagation guarantee is ≤1 minute (60-second polling). Scenarios using "30 seconds ago" would produce non-deterministic (flaky) tests since dependent apps may not have polled yet.
- **Note**: The concurrent-edit edge case ("This setting was updated by [admin email] 30 seconds ago") was intentionally left unchanged as it refers to admin UI conflict detection, not propagation.

### Issue 6 — FR-024 and FR-011 Moved to New "Downstream Consumers" Section

- **Section**: Dependencies
- **Change**: Removed FR-024 and FR-011 from Internal Dependencies; added a new "Downstream Consumers" sub-section above External Dependencies listing them with corrected relationship descriptions
- **Reason**: FR-026 provides infrastructure that FR-024 and FR-011 consume — listing them as dependencies of FR-026 reversed the dependency direction and would incorrectly imply FR-026 is blocked by those modules.

### Issue 7 — Seeding Data "Friend Recommendation" → "Friend Referral"

- **Section**: Implementation Notes → Initial Configuration / Seeding
- **Change**: Discovery Questions Initial Option 3: `"Friend Recommendation"` → `"Friend Referral"`
- **Reason**: Workflow A3 (line 181) and User Story 4 (line 944) both use "Friend Referral". The seeding data used a different label, creating a data inconsistency between what would be seeded in the database and what workflows and tests expect to find.

### Issue 8 — FR-003 Module Name Corrected in Dependencies

- **Section**: Dependencies → Internal Dependencies
- **Change**: `FR-003 / Module P-02: Inquiry Submission & Distribution` → `FR-003 / Module P-02: Quote Request & Management`
- **Reason**: "P-02: Quote Request & Management" is the canonical module name per system PRD. "Inquiry Submission & Distribution" is the FR feature name, not the module name.
