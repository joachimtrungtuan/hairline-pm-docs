# FR-013 Moderation Gate Removed

**Date**: 2026-03-03
**Report Type**: PRD Revision — Transcription Alignment
**Affected Documents**:
- `local-docs/project-requirements/functional-requirements/fr013-reviews-ratings/prd.md`
- `local-docs/reports/2026-02-05/missing-mobile-flows-design-complement.md` (P05.3 flow)

---

## Summary

Removed the pre-publication moderation gate from FR-013 (Reviews & Ratings). Client transcriptions were reviewed and confirmed that no moderation workflow was requested. Reviews now publish immediately upon patient submission. Admin retains the ability to edit or remove published reviews post-publication for policy violations.

## Transcription Evidence

- **AdminPlatform-Part1 (lines 91–100)**: Client discusses admin ability to **add/seed** reviews for new providers (authenticated reviews from external sources), not moderate patient-submitted reviews before publication.
- **AdminPlatform-Part1 (lines 103–110)**: Client states data should never be permanently deleted — "archived somewhere" — with 7-year legal retention. This supports the retention policy but says nothing about moderation.
- **HairlineApp-Part1 (lines 232–248)**: Client describes the review submission flow as straightforward — patients leave reviews and they appear on clinic/provider profiles. No mention of a moderation gate.
- **No transcription** across all 7 files mentions "moderation", "approve before publish", "review queue", or any pre-publication review gate.

## Conclusion

The moderation workflow (Submit → Pending Moderation → Admin Approves → Published) was an AI-generated addition not based on client requirements.

---

## Changes Made

### FR-013 PRD (v1.1 → v1.2)

| Section | Change |
|---------|--------|
| Executive Summary | Removed "subject to admin moderation before publication"; added "published immediately upon submission" |
| Multi-Tenant Architecture | Patient: removed "view status (pending/approved/rejected), edit prior to moderation"; Admin: changed from "Moderate incoming reviews" to "Monitor published reviews, edit or remove post-publication" |
| Multi-Tenant Breakdown — Patient | Reviews published immediately; patient can edit at any time |
| Multi-Tenant Breakdown — Admin | Changed from moderation queue to review management dashboard + post-publication edit/remove + seed reviews |
| Entry Points | "Moderation" → "Review Management" |
| Backlog | Admin-seeded reviews moved to main scope (per client transcription) |
| Main Flow | Review published immediately on submission (no Pending Moderation status) |
| A1 | Replaced "Admin Moderation – Approve" with "Admin Removes a Published Review (Post-Publication)" |
| A2 | Replaced "Admin Moderation – Reject/Request Edits" with "Admin Edits a Published Review (Post-Publication)" |
| Screen 1 Business Rules | "editing allowed until moderation starts" → "patient can edit their published review at any time" |
| Screen 2 | Renamed from "Admin – Moderation Queue" to "Admin – Review Management"; actions changed from Approve/Reject to Edit/Remove; added "Add Review" for seeding |
| General Module Rules | Removed moderation references; patient can edit published review at any time |
| Data & Privacy Rules | "redact or reject" → "redact or remove post-publication" |
| Admin Editability | "moderation reasons catalogue" → "removal reasons catalogue" |
| Configurable | "auto-hold rules" → "auto-flag rules for admin review" |
| Moderation Policy Notes | Renamed to "Admin-Seeded Review Policy" |
| Admin Metrics | SC-006: "moderation decision" → "flagged review decision"; SC-007: "moderator" → "admin identity" |
| Dependencies | Notifications updated for removal and response alerts |
| Assumptions | Removed moderation references |
| Implementation Notes | Removed pending/published separation |
| User Story 1 | Review published immediately (not saved as Pending) |
| User Story 2 | Changed from "Admin approves" to "Admin removes a published review" |
| Edge Cases | "queue for moderation" → "auto-flag for admin review post-publication" |
| REQ-013-003 | "admin moderation with approve/reject" → "publish immediately, admin post-publication edit/remove" |
| REQ-013-004 | "publish approved reviews" → "display published reviews; admin-removed reviews unpublished and archived" |
| Unclear Requirements | Updated to reflect no-moderation model |
| Key Entities | ModerationDecision → AdminAction; Review status values: Published / Removed by Admin |

### Design Complement Report (P05.3)

| Section | Change |
|---------|--------|
| P05.3 Flow Diagram | Removed moderation check branch; reviews publish immediately; edit available for Published status; Request Takedown available for Published status; Removed by Admin shown read-only |
| P05.3-S1 Status Badge | "Published / Pending Moderation / Rejected" → "Published / Removed by Admin" |
| P05.3-S1 Business Rules | Added "Reviews are published immediately upon submission"; removed Pending Moderation and Rejected status explanations; added "Removed by Admin" explanation |
| P05.3-S2 Status Badge | "Published / Pending Moderation / Rejected" → "Published / Removed by Admin" |
| P05.3-S2 Rejection Reason | Replaced with "Admin Removal Reason" |
| P05.3-S2 Edit Review | Removed moderation gate; visible for Published reviews; edits published immediately |
| P05.3-S2 Request Takedown | Visible only for Published reviews |
| P05.3-S2 Business Rules | Removed all moderation gate references; patient can edit at any time while Published; admin can edit/remove post-publication |

---

**Version**: FR-013 v1.2
**Author**: Product alignment (2026-03-03)
