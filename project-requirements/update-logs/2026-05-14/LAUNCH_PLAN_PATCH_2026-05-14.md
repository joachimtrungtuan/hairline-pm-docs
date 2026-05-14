# Launch Plan Patch — May 14, 2026

**Type:** Document Revision
**File:** `local-docs/product-plans/2026-05-13/launch-plan.md`
**Prepared By:** Product Manager

---

## Summary

Patched the Hairline Platform Launch Plan to resolve logical loopholes identified in a full audit. Seven coordinated changes restructure module sequencing, ceremony timing, App Store schedule, regression load distribution, and launch framing. The plan now operates as a soft launch for vendor demonstrations (not a full public launch), with a strict no-weekend-work policy and front-loaded Sprint 1.

## Patch Summary

### Patch 1 — Sprint 1: Pulled in Auth + Onboarding

Moved into Sprint 1: **P-01 Auth & Profile Management**, **PR-01 Auth & Team Management**, **A-02 Provider Management & Onboarding**. Sprint 1 is now self-contained — full patient registration → inquiry → quote → booking → treatment → aftercare journey is testable end-to-end. Sprint 1 DoD gained three new verification bullets.

### Patch 2 — Sprint 2: Pulled in Payment Sub-features

Moved into Sprint 2: **P-03b Payment Sub-features** (installment plan enrollment, multi-currency display, receipt download, refund request). Sprint 1 now ships P-03a (core booking + base-currency deposit); Sprint 2 ships the sub-features close behind. Sprint 4 DoD no longer mentions P-03b.

### Patch 3 — App Store Gantt Cleanup

- Account setup trimmed from 9d to 5d (account creation does not need 9 days).
- Beta build schedule reconciled to single submission day **June 4** (overall and Sprint 3 inner Gantts were inconsistent).
- Final build submission moved from **June 10–11 → June 9 (Tue)**, giving Apple 4 full business days of review before launch instead of 3.
- Store approval window extended to **June 10–14 (5 days)**.

### Patch 4 — Sprint Planning to Friday + Zero Weekend Work

- Sprint Planning relocated from Sunday (May 24 / May 31 / June 7) to **Friday of previous sprint, after Review + Retro**: Fri May 22 (Sprint 2), Fri May 29 (Sprint 3), Fri June 5 (Sprint 4), Fri June 12 (Sprint 5).
- Sprint 4 work that previously fell on Sat June 13 (DNS pre-check, smoke test, pre-launch checklist) absorbed into Sprint 4 working days (DNS pre-check → Thu June 11; smoke test + pre-launch checklist → Fri June 12).
- Sat–Sun June 13–14 marked as no-team-work (PM monitors store approval inbox only).
- Sprint 4 header dropped the "*+ June 13 (Sat) pre-launch buffer*" note.

### Patch 5 — Spread Sprint 4 Load Back into Sprint 3

- Added **Cumulative Regression QA (Sprint 1 + Sprint 2 modules)** to Sprint 3 last two days (June 4–5).
- Sprint 4's full regression replaced with **Final Integration Regression** scoped to Sprint 3 + Sprint 4 modules and cross-tenant flows only.
- Client UAT moved earlier (June 10–11 Wed–Thu) instead of June 11–12, freeing Fri June 12 for regression + pre-launch + ceremonies.
- Final App Store build submission moved to Tue June 9 (day after Stakeholder Review).

### Patch 6 — Soft Launch Reframe + Minimal Safeguards

- Added an Overview callout reframing June 15–16 as a **soft launch for vendor demonstrations and business collaboration discussions** — not a full public consumer launch.
- Added a weekend policy statement (no Sat/Sun work; Sprint Planning on previous Friday).
- Added three minimal safeguards to the Go-Live Checklist: (a) production database backup before migration, (b) previous deployment artifact tagged for rollback, (c) explicit **Go/No-Go decision point** by PM after smoke test, before App Store release trigger.
- Removed formal hypercare from the Launch Day Gantt (not needed for soft launch); kept basic monitoring.

### Patch 7 — Cleanup

- Stripped misleading `:done` markers from Sprint 1 dev/QA, Sprint 2 / 3 / 4 planning bars in Master Gantt (these were colour hacks but read as "already finished").
- Added explicit submodule callouts where Sprint 1 DoD references them: P-03a, P-05/P-05b, PR-02/PR-02b.
- Non-Dev Milestones: assigned **PM (monitoring)** as owner for "App Store approvals received" (was blank `—`); added new milestone rows for cumulative regression (June 5), final integration regression (June 12), DNS pre-check (June 11).

## Final Sprint Allocation

| Sprint | Theme | Modules (new) |
|--------|-------|----------------|
| Sprint 1 (May 14–22) | Core + Auth | P-01, P-02, P-03a, P-05, P-07, PR-01, PR-02, PR-03, PR-04, A-01, A-02, A-03, A-09a, S-01, S-02, S-05 |
| Sprint 2 (May 25–29) | Config + Payment Sub-features | P-03b, P-04, PR-06, A-09b, A-09c (Part 1), S-04 |
| Sprint 3 (June 1–5) | Peripheral + Cumulative Regression | P-06, P-08, PR-07, A-06, A-09c (Part 2), A-10, S-03 |
| Sprint 4 (June 8–12) | Wrap-Up + UAT + Final Integration Regression | PR-05, A-04, A-05, A-07, A-08, S-06 |
| Launch (June 15–16) | Soft launch — vendor demonstrations | — |

## Key Date Changes

| Item | Before | After |
|------|--------|-------|
| Final App Store build submission | June 10–11 | **June 9 (Tue)** |
| Store approval window | June 13–14 (2d) | **June 10–14 (5d)** |
| Sprint 2 Planning | Sun May 24 | **Fri May 22** |
| Sprint 3 Planning | Sun May 31 | **Fri May 29** |
| Sprint 4 Planning | Sun June 7 | **Fri June 5** |
| Sprint 5 Planning | n/a | **Fri June 12** |
| Pre-launch checks | Sat June 13 + Sun June 14 | **Fri June 12** (in Sprint 4) |
| Client UAT | June 11–12 | **June 10–11** |
| Full Regression | June 12 (1 day, all modules) | Split: **June 4–5 (S1+S2)** + **June 12 (S3+S4+integration)** |

## Source Documents

- `local-docs/product-plans/2026-05-13/launch-plan.md` — patched in place
- `local-docs/project-requirements/update-logs/2026-05-13/LAUNCH_PLAN_2026-05-13.md` — original creation entry
