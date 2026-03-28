---
date: 2026-03-28
type: major
fr: FR-001
module: P-01 Auth & Profile Management
author: AI
---

# FR-001 Screen Restructure & Renumber — 2026-03-28

## Summary

Corrected a misclassification in the Screen Specifications section: Screens 14–19 (patient profile, settings, and account management flows) were incorrectly placed under the `### Admin Platform Screens` heading. Only Screen 13 (Patient Management Dashboard) is a genuine admin screen.

## Changes Applied

### 1. Section restructure (fr001-patient-authentication/prd.md)

- Removed the `### Admin Platform Screens` divider from between Screen 12 and the profile/settings screens
- Moved the old Screen 13 (Patient Management Dashboard) and its `### Admin Platform Screens` heading to the end of the Screen Specifications section, after all patient screens
- All patient screens now appear contiguously under `### Patient Platform Screens`

### 2. Screen renumbering

| Old Number | New Number | Screen Title |
|------------|------------|--------------|
| Screen 13 (Admin) | Screen 19 | Patient Management Dashboard |
| Screen 14 | Screen 13 | Profile Overview (Patient) |
| Screen 15 | Screen 14 | Edit Profile |
| Screen 16 | Screen 15 | Settings Main Screen |
| Screen 16a | Screen 15a | Notification Settings |
| Screen 16b | Screen 15b | Privacy & Security Menu |
| Screen 16c | Screen 15c | Privacy Policy |
| Screen 16d | Screen 15d | Terms & Conditions |
| Screen 17 | Screen 16 | Delete Account (Deletion Request / DSR) |
| Screen 18 | Screen 17 | Change Password |
| Screen 18a | Screen 17a | Password Changed Confirmation |
| Screen 19 | Screen 18 | Identity Re-verification (Shared Component) |

Final screen sequence: Patient Platform Screens 1–18 (sequential, no gaps), Admin Platform Screen 19.

### 3. Internal cross-references updated (prd.md)

All navigation references within screen specs (back arrows, modal routing, shared component callouts) and the Appendix Change Log updated to new numbers.

### 4. External documents updated

| File | Change |
|------|--------|
| `update-logs/README.md` | Screen 14/16 → 13/15 in index entry |
| `update-logs/2025-10-30/FR001_PRD_VERIFIED_2025-10-30.md` | Screen 14 → 13, Screen 16 → 15 |
| `update-logs/2026-02-05-cancel-inquiry-fr-updates.md` | Screen 14 → 13, Screen 16 → 15 |
| `task-creation/2025-11-14/implementation-tasks-2025-11-14.md` | Screen 14 → 13 |
| `task-creation/2025-12-01/implementation-tasks-2025-12-01.md` | Screen 14 → 13, Screen 16 → 15; URL anchors updated |
| `reports/2026-02-05/missing-mobile-flows-design-complement.md` | FR-001 Screen 14 → 13 (6 hits), FR-001 Screen 16 → 15 (9 hits) |
| `reports/2026-02-05/cancel-inquiry-fr-impact-report.md` | Screen 14 → 13, Screen 16 → 15 |
| `reports/2026-03-17/mobile-estimate-cross-check-findings.md` | FR-001 Screen 16 → 15 |

### 5. Not affected

- FR-011, FR-033, and all other FRs have independent screen numbering; their Screen 13–19 references are for their own screens and were not changed.
- Screens 1–12 (auth/onboarding) were not renumbered.
- FR-020 references FR-001 settings by name only (no screen number); no change needed.

---

## Addendum: Data Fields Table Standardisation

All 14 screens that had bullet-list `**Data Fields**` sections were converted to the standard 5-column table format required by `prd-template.md`:

| Field Name | Type | Required | Description | Validation Rules |

**Screens converted** (previously bullet-list, now table):

Screens 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 16, 19

**Screens already compliant** (no change):

Screens 15, 15a, 15b, 15c, 15d, 17, 17a, 18

No business rules, acceptance scenarios, or content logic were altered — only the Data Fields presentation format was standardised.
