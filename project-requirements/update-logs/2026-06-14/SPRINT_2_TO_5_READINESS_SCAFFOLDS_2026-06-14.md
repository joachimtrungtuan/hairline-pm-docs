# Sprint 2–5 Readiness Scaffolds

**Date:** 2026-06-14
**Type:** Major update (new readiness reports)
**Source skill:** `sprint-readiness-reporting` (Flow 1 — Create Scaffold From Launch Plan)
**Source launch plan:** `local-docs/product-plans/2026-05-13/launch-plan.md`

## Summary

Created sprint readiness & fix-backlog scaffolds for all remaining sprints (Sprint 2 through the Launch sprint), copying the structure of the existing Sprint 1 report and the bundled template, and anchoring each scaffold's scope, modules, user stories, and deferrals to the corresponding section of the launch plan.

Per the user's instruction, the scaffolds are **not** placed in today's date folder. Instead they are dated using the May 29 Sprint 1 milestone as the first anchor and stepping one week forward, evenly spaced — which lands exactly on the launch plan's actual Sprint Review milestone dates for Sprints 2–4. Sprint 5 (Launch) uses its real launch date (June 22) rather than the even-week date, per user decision.

## Files Created

| File | Sprint | Folder Date | Notes |
|---|---|---|---|
| `local-docs/product-plans/2026-06-05/sprint-2-readiness-fix-backlog.md` | Sprint 2 — Config & Aftercare | 2026-06-05 | Matches launch-plan Sprint 2 Review date. |
| `local-docs/product-plans/2026-06-12/sprint-3-readiness-fix-backlog.md` | Sprint 3 — Peripheral | 2026-06-12 | Matches launch-plan Sprint 3 Review date. |
| `local-docs/product-plans/2026-06-19/sprint-4-readiness-fix-backlog.md` | Sprint 4 — Wrap-Up | 2026-06-19 | Matches launch-plan Sprint 4 Review date. |
| `local-docs/product-plans/2026-06-22/sprint-5-readiness-fix-backlog.md` | Sprint 5 — Launch | 2026-06-22 | Uses real launch date; adapted template for a launch event (activities/smoke-test flows instead of modules). |

## Scope Filled Per Scaffold

Each scaffold has its Document Control & Sprint Summary, Modules In Scope (Section 1.1), User Stories In Scope (Section 1.2), and Explicitly Deferred / Out Of Scope (Section 1.3) filled from the launch plan, plus Section 2.1 sprint-level blockers and Section 2.2 per-module evidence-gap rows seeded as `Review pending`. Section 3 captures launch-plan deferrals.

- **Sprint 2** — 9 modules (P-03b, P-04, P-05, PR-04 travel, PR-04 aftercare, A-03, A-09b, A-09c Part 1, S-04); deferrals include admin travel oversight (Sprint 4), notification delivery verification (Sprint 3), and A-09c Parts 2/3.
- **Sprint 3** — 14 modules (P-06, P-08, P-02/PR-06 reviews, P-03, P-01, PR-07, PR-06, PR-02/PR-05, A-06, A-09c Part 2, A-09, A-10, A-01, S-03); deferrals include FR-012 messaging search/filter, patient provider-discovery search, admin DSR actioning (Sprint 4), and A-09c Part 3.
- **Sprint 4** — 12 modules (PR-05, PR-06 i18n, A-04, A-05, A-07, AF-01, A-08, A-09c Part 3, A-01 i18n/DSR, Search & Filtering, S-02/S-03, S-06); deferrals include FR-036, patient provider-discovery search, travel dispatch ops, and post-RC-freeze mobile code.
- **Sprint 5 (Launch)** — adapted: Section 1.1 lists the go-live checklist activities and the eight critical smoke-test flows; Section 2 tracks go/no-go gates and per-flow production-verification placeholders; deferrals include post-freeze mobile code and beta/internal store fallback.

## Notes

- No staging or product review was performed in this pass; all module/flow rows are readiness evidence gaps (`Review pending`), not confirmed product defects.
- Evidence links are `TBD`; persistent uploaded URLs must be added during real review.
