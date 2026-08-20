# FR-037 Advice, Preview, and Dashboard Revision

**Date**: 2026-08-20
**Document**: `functional-requirements/fr037-monitor-hair-loss/prd.md` (v1.3 → v1.4)
**Trigger**: Product-owner feedback on provider advice records and windows, pre-assignment provider review, and Provider/Admin monitoring screens

---

## Context

The previous draft did not define whether provider advice belonged to a patient log, treated an advice window as generally time-limited, and gave Provider/Admin listing and detail screens only summary-level field coverage. It also omitted the Admin’s need to share limited case information with a candidate provider before assignment.

## Changes Applied

### 1. Advice is a separate calendar record

- A submitted provider comment creates its own provider-authored entry in the case tracking calendar.
- Advice is never attached to, stored inside, or used to mutate a patient-authored daily log, including when both records share a date.
- Submitted advice can be edited. Patient, Provider, and Admin views show an edited cue and latest-edit timestamp; immutable versions remain in the audit trail.

### 2. Advice-window lifecycle

- Each window becomes actionable on its calculated start date and has no ordinary submission deadline.
- The window stays available until its one advice entry is submitted.
- The only expiry case is supersession: when a new window opens before the old one was used, the old window expires and the new window becomes the sole actionable window.
- Provider review shows the current window and the immediately superseded missed window together with distinct states.

### 3. Expiring pre-assignment preview without embedded chat

- Admin can generate a read-only, revocable case-preview link for a candidate provider before assignment or reassignment.
- Admin selects the expiration period each time the link is created.
- Preview access is scoped, audited, and assignment-neutral; opening the link grants no ongoing case access.
- Admin and provider may communicate through an existing external channel, but FR-037 adds no chat screen.

### 4. Provider screens expanded

- Screen 8 now requires scoped search, status/advice/assignment filters, sorting, and pagination.
- Screen 9 now mirrors the patient-visible monitoring dashboard, calendar, and day-level log detail while adding a distinct provider-only advice area and advice-window stack.

### 5. Admin screens expanded

- Screen 11 now includes All Cases, Self-Monitoring, and Provider Intervention tabs; patient/case/provider search; operational filters and sorting; and case, activity, assignment, advice, and preview summaries.
- Screen 12 now presents the patient-parity case header, intake and medical data, monitoring dashboard, full calendar, daily logs, scans, exports, and conversion data, plus Admin-only assignment, preview, advice-window, and audit controls.

## Validation

- Confirmed the PRD retains the standard Patient, Provider, and Admin screen ownership sections and Screens 1–12.
- Checked the changed Markdown for malformed tables and whitespace errors.
- Confirmed advice separation, window supersession, preview expiry, search/filtering, and patient-parity detail are each represented in rules, screens, acceptance scenarios, requirements, and entities.
