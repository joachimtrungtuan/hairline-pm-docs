# P-05 Flows Design Complement — Update Log

**Date**: 2026-03-03
**Report Type**: Design Specification Update
**Author**: Claude Code
**Target Document**: `local-docs/reports/2026-02-05/missing-mobile-flows-design-complement.md`

---

## Summary

Filled in all three P-05 (Aftercare & Progress Monitoring) placeholder flows in the Missing Mobile Flows Design Complement report. All Mermaid flow diagram placeholders and HTML comment screen spec placeholders replaced with complete, source-grounded content.

---

## Changes Made

### Flow P05.1: Day-to-Day Treatment Progress

**Related FRs**: FR-010 (Treatment Execution), FR-011 (Aftercare Recovery Management)

- **Flow Diagram**: Replaced `%% PLACEHOLDER` Mermaid stub with a `flowchart TD` showing: notification trigger → patient opens case → Treatment Progress Timeline (P05.1-S1) → tap day row → Day Details Popup (P05.1-S2) → real-time sync updates → case transitions to Aftercare on treatment completion.
- **Screen P05.1-S1 (Treatment Progress Timeline)**: Filled in 11-field spec table sourced from FR-010 Screen 1 (In Progress Case View). Key fields: Case Status Badge, Provider/Clinic Name, Treatment Name, Package Name (conditional), Assigned Clinician, Procedure Date, Estimated Graft Count, Beginning Note (conditional), Overall Progress, Treatment Days List, Journey Timeline, Contact Provider action.
- **Screen P05.1-S1 Business Rules**: 5 rules sourced from FR-010 patient platform architecture: real-time status sync via server push; provider clinical notes never visible to patient; Beginning Note hidden if absent; progress auto-calculation formula; all fields read-only.
- **Screen P05.1-S2 (Day Details Popup)**: Filled in 5-field spec table sourced from FR-010 Screen 2 (Day Details Popup). Fields: Day Label, Scheduled Date, Day Description, Status Badge (with real-time sync note), Close action.
- **Screen P05.1-S2 Business Rules**: 5 rules including real-time status sync, provider notes hidden, read-only popup, status color coding (grey/blue/green/amber/red), accessibility for all days regardless of status.

### Flow P05.2: Previous Treatments List

**Related FRs**: FR-010 (Treatment Execution), FR-011 (Aftercare Recovery Management)

- **Flow Diagram**: Replaced `%% PLACEHOLDER` stub with a `flowchart TD` showing: navigate to My Treatments → list view (P05.2-S1) → filter/sort/search actions → tap treatment card → case detail view; also shows "Leave a Review" CTA path to FR-013 flow.
- **Screen P05.2-S1 (My Treatments List)**: Filled in 13-field spec table. Key fields: Screen Title, Filter Tabs (All/In Progress/Completed/Cancelled), Search Bar, Sort Options, and treatment card fields: Treatment Name, Provider Name & Avatar, Treatment Dates, Status Badge, Progress Indicator (conditional), Outcome Summary (conditional), Cancellation Reason (conditional), Leave Review CTA (conditional), Empty State.
- **Screen P05.2-S1 Business Rules**: 5 rules: In Progress pinned to top of All tab; default sort most recent first; cancellation reason inline; Leave Review CTA eligibility logic (status=Completed + ≥3 months per FR-013 + no review yet); all cards tappable.

### Flow P05.3: Submitted Reviews List

**Related FRs**: FR-013 (Reviews & Ratings)

- **Flow Diagram**: Replaced `%% PLACEHOLDER` stub with a `flowchart TD` showing: navigate to My Reviews → list view (P05.3-S1) → sort action → tap review card → Review Detail View (P05.3-S2) → edit window check → edit/delete paths with confirmation prompt.
- **Screen P05.3-S1 (My Reviews List)**: Filled in 8-field spec table sourced from FR-013 patient view. Fields: Screen Title, Sort Options, and review card fields: Treatment Name, Provider Name & Avatar, Overall Star Rating, Review Date, Review Excerpt (2-line truncated), Status Badge (Published/Pending Moderation/Rejected), Empty State.
- **Screen P05.3-S1 Business Rules**: 5 rules: FR-013 time-gating (≥3 months); Published reviews visible to others; Pending Moderation awaiting admin; Rejected may be resubmitted; default sort most recent first.
- **Screen P05.3-S2 (Review Detail View)**: Filled in 13-field spec table. Fields: Treatment Name, Provider Name & Avatar, Overall Star Rating (large), Category Ratings (Facility/Staff/Results/Value), Review Text, Review Submission Date, Review Photos (gallery), Moderation Status Badge, Rejection Reason (conditional), Provider Response (conditional), Edit Review (conditional), Delete Review, Back Navigation.
- **Screen P05.3-S2 Business Rules**: 5 rules sourced from FR-013: Edit visible only while Pending Moderation and no admin action; editing resets to Pending Moderation; Delete requires confirmation and is permanent; Provider responses read-only for patient; Category ratings from FR-013 Screen 1.

---

## Status Updates

| Flow | Before | After |
|------|--------|-------|
| P05.1 in Summary Dashboard | 🔴 Not Designed | 🟡 Specified |
| P05.2 in Summary Dashboard | 🔴 Not Designed | 🟡 Specified |
| P05.3 in Summary Dashboard | 🔴 Not Designed | 🟡 Specified |
| P05.1 flow header | 🔴 Not Designed | 🟡 Specified |
| P05.2 flow header | 🔴 Not Designed | 🟡 Specified |
| P05.3 flow header | 🔴 Not Designed | 🟡 Specified |

---

## Source References

- `local-docs/project-requirements/functional-requirements/fr010-treatment-execution/prd.md` — Patient Platform Screens (Screen 1: In Progress Case View, Screen 2: Day Details Popup), Multi-Tenant Architecture section
- `local-docs/project-requirements/functional-requirements/fr011-aftercare-recovery-management/prd.md` — Module Scope (Patient Platform entry points and aftercare activation trigger)
- `local-docs/project-requirements/functional-requirements/fr013-reviews-ratings/prd.md` — Screen 1 (Patient Submit Review), Business Rules (eligibility, time-gating, edit policy, moderation states)
