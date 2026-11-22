# Owner Answers After the Phase 4 Re-check — Applied to PRDs and Graph

**Date:** 2026-11-22
**Type:** Major update — wording changes in 10 PRDs and matching requirements graph changes
**Programme:** `plans/261108-1040-requirements-graph-programme/` (Hairline root), Phase 4 (now closed)
**Decisions record:** `plans/reports/owner-decisions-261121.md` (Hairline root), section "Owner answers (2026-11-22)"
**Change Requests:** none. Programme rulings set the new baseline, so each change is recorded in the PRD's Appendix: Change Log only.

## Summary

The owner answered the 17 items left by the completeness re-check of 2026-11-21. Fifteen needed changes; two (layout lines, merged aftercare pairs, and FR-031 and FR-003 wording that already matched) needed none. All are applied. Graph lint stays at 102 findings (90 Phase 8 hand-offs, 10 accepted, 2 known); no live node points at a retired node.

## What changed

| Item | Answer | PRD change | Graph change |
|------|--------|------------|--------------|
| 1, 16 | Notification Events belong to FR-030; a separate "Email change code sent" Event | None | 55 Events moved to FR-030; `EVT-email-change-otp-sent` added |
| 2 | Patient sees certifications and awards, never the license number | FR-005 v3.1: Screen 1 field, Comparison Differentiators, REQ-005-014 | License `shows` link removed from `SCR-005-01`; REQ-005-014 |
| 3 | Installment default notifies admin, patient and provider | FR-006 v2.13 edge case; FR-007B v1.7 flow B2, retry rule, acceptance scenario, REQ-007b-020 | REQ-006-080, REQ-007B-020 |
| 4 | A Manager changes roles only of members below Manager | FR-009 v1.9: REQ-009-004, Screen 6 rule, stale "Admin" wording | REQ-009-004, REQ-009-104 |
| 5 | Owner handover stays in FR-009: active member, old Owner becomes Manager, reason, both emailed | FR-009 v1.9: Rule 11, REQ-009-174 | REQ-009-174 |
| 6 | Extra patient documents: PDF and image files only, at most 5 | FR-016 v1.12: Medical Data tab | REQ-016-200 reworded; new REQ-016-216 |
| 7 | Percentage 1 to 100 under a cap starting at 50 percent; fixed amount above 0, no cap | FR-019 v2.7: Screen 2 and 9 Value, Admin Editability | REQ-019-114; `SET-promotion-max-discount-value` default 50 percent |
| 8 | Overdue is a calculated flag, not a plan status | FR-022 v2.20: FR-007b Screen 5 filters, status reference | REQ-022-101 |
| 9 | After a media retry the treatment takes the status the admin picks | FR-024 v1.7: edge case | New REQ-024-100 |
| 10 | Country flag is required; admin uploads it (FR-026 Screen 4) | FR-026 v1.15: REQ-026-011 | REQ-026-011; `ENT-country.flag_url` required |
| 11 | FR-026 owns the problem-duration list with five starting values | FR-026 v1.15: Screen 5c, new REQ-026-139 | New `SET-problem-duration-options`, REQ-026-139; REQ-003-122 linked |
| 12 | One shared failed-login setting | FR-026 v1.15: Screen 8 field removed, Screen 2 note, REQ-026-116 | `SET-admin-max-failed-logins` retired; REQ-026-116, REQ-031-099 use `SET-max-login-attempts` |
| 13 | Built-in support categories and priorities stay locked | FR-034 v2.6: Admin Editability list | REQ-034-087 |
| 14 | 100 to 200 cases a day at launch, 500 at peak, 1000 within 12 months | FR-034 v2.6: REQ-034-069 | REQ-034-069 |

## Files

- PRDs: fr005, fr006, fr007b, fr009, fr016, fr019, fr022, fr024, fr026, fr034 (each with a 2026-11-22 line in Appendix: Change Log).
- Graph change-sets: `graph/changesets/2026-11-22-owner-answers-events.yaml`, `-batch1.yaml`, `-batch2.yaml`, `-batch3.yaml`; `graph.db` and `graph.json` re-exported.

## Follow-up (implementation backlog)

- Country flag is now required: the starting country list and the bulk CSV import (FR-026 Screen 4) need a flag for every country.

## Audit follow-up (same day)

An independent review of Phase 4 against its Definition of done found the phase met, with wording left over from the old text. Fixed:

- FR-026 v1.16: the Country entity lists `flag_url` as required, matching Screen 8.
- FR-009 v1.10 (proposed): the remaining "Admin" wording for the provider role is now "Manager" (department field, Privacy Rule 2, two role-change scenarios); Screen 3 states that a Manager can change the role of Clinical Staff and Billing Staff only.
- FR-005 v3.2: the FR-015 dependency line no longer mentions licenses.
- FR-030 v1.19: the email change code has its own row in the notification catalogue (`account.email_change_code`).
- Graph (`graph/changesets/2026-11-22-audit-leftovers.yaml`): Rule texts REQ-019-093, REQ-009-103 and REQ-009-155 now match the PRDs.
- "Last Updated" footers of the PRDs edited today now read 2026-11-22.
