# Launch Plan Review & Coverage Rework — May 20, 2026

**Type:** Document Revision (PRD/FR alignment + structural changes)
**File:** `local-docs/product-plans/2026-05-13/launch-plan.md`
**Prepared By:** Product Manager (with subagent-assisted FR cross-check)

---

## Summary

Three coordinated tracks of review work applied to the Launch Plan: (1) PRD/FR cross-check of every sprint via Haiku subagents against all 36 FRs — used to expand User Stories and Definition of Done with previously thin or missing coverage; (2) timeline logical-consistency audit applied as five targeted fixes; (3) Sprint Calendar drift check (no drift found). Additionally, the Modules sections of all four sprints were restructured into a `Tenant | Modules | FR(s) directly affected` table, and three orphan FRs were allocated across Sprints 3–4.

Follow-up correction pass on May 20 after a full plan review: timeline contradictions were resolved around release-candidate submission, store-review fallback, Sprint 4 code freeze, Sprint 2 App Store creative deliverables, UAT triage, and launch smoke coverage. FR/module mapping and DoD were corrected for FR-002, FR-003, FR-006, FR-007/007b, FR-008, FR-011, FR-012, FR-013, FR-014, FR-017, FR-018, FR-019, FR-021, FR-022, FR-023, FR-032/033/034/035, and a topline-only FR-036 placeholder. The integrated full-lifecycle user story was not finalised in this patch because provider payout timing requires user confirmation against current FR-017 behavior.

---

## Track 1 — PRD/FR Cross-Check & Story/DoD Rework

**Method:** Four Haiku Explore subagents ran in parallel (one per sprint), each cross-checking the sprint's modules against every relevant FR file in `local-docs/project-requirements/functional-requirements/`. Sprint 1 agent re-run with explicit module→FR mapping after the first pass misidentified module names. All findings synthesised in-session (no agent-output files created).

**Sprint 1 rework (per agent v3 findings):**
- DoD reorganised into Sprint-level gates + per-module sections, each with explicit FR citation
- Coverage added: inquiry cancellation cascade (FR-001), refund tier policy (FR-007), pre-payment anonymization (FR-024/032), first-login tour, task transfer
- Clinic profile DoD expanded with full tab coverage (Languages, Awards, Documents) per FR-002
- New User Stories added for questionnaire/legal document/OTP config (A-09a) and shared-services foundations (S-01, S-02, S-05)

**Sprint 2 rework:**
- P-03b expanded with FR-007b retry/grace logic, grace-period notifications, refund-tier policy enforcement, FX disclosure
- P-04 split into Path A (provider-included) and Path B (self-booked) per FR-008
- **P-05 standalone aftercare path added** (previously missing): purchase → admin assigns provider → activation, plus 48-hour escalation rule per FR-011
- A-09c Part 1 expanded with Stripe pre-save API test, currency-pair sequencing, FX sync scheduling, regional alignment to FR-028
- A-09b: template approval workflow for provider-submitted variants noted
- Audit-log gate added at sprint level for all financial mutations (FR-029)

**Sprint 3 rework:**
- **A-10 stories added in full**: automatic keyword flagging, "Hairline Admin" emergency intervention with mandatory reason logging, support escalation
- PR-07 outgoing call DoD made explicit (was implicit before)
- P-08 expanded to bind FR-035 (patient support) to FR-033 (help centre management) and FR-034 (ticketing)
- **fr013 Reviews & Ratings integrated** into Sprint 3 via P-02/PR-06 (submission + response) and A-01 (moderation queue, takedown, authenticated insertion)
- S-03 expanded with per-channel telemetry visibility (sent/delivered/failed/bounced)

**Sprint 4 rework:**
- **PR-05 full story + DoD authored** (was thin): cockpit, funnel, patient analytics, finance/payouts with 3-day buffer, pricing benchmarks, exports
- **A-07 full story + DoD authored** (was thin): CRUD, commission auto-calc, monthly-on-7th payout with £50 threshold + roll-over, discount-code attribution
- **A-04 full story + DoD authored** (was thin): admin travel queue, transfer assignment, daily logistics view
- A-05 expanded into a/b/c sub-modules: patient billing, provider payouts (3-day buffer + cron auto-process), affiliate billing, discount reconciliation, FX alerts
- A-08 expanded across all seven analytics surfaces per FR-014
- **FR-021 i18n added across tenants** as new orphan-fill: P-01 patient switch, PR-06 provider switch, A-09c Part 3 admin authoring (registry, JSON import/export, version + rollback, coverage report)
- **FR-023 compliance added** as Sprint 4 peripheral: data retention per category, 7-year retention for medical/financial, GDPR/DSR workflow with SLA timer
- **FR-022 search & filtering added** as cross-cutting P1 MVP scope (provider + admin list views; patient help/ticket only; provider-discovery search remains P2)
- S-06 Audit Log Service formalised: append-only writes, retention enforcement, tamper-evident export bundles

---

## Track 2 — Timeline Logical-Consistency Fixes

Five issues confirmed by audit; all fixed in place:

1. **Launch Day Gantt labels** — clarified Production Deployment vs. Launch Smoke Test vs. App Store Release Trigger to remove ambiguity between staging/pre-prod and production smoke checks
2. **Sprint 1 inner Gantt dev1 bar** — extended from 7d → 9d to align with the new May 21 dev-start while preserving the May 22 Kickoff ceremony date
3. **Master Timeline** — June 16 app-build milestone added to mirror the Sprint 4 Gantt; later follow-up reframed this as release-candidate build cutoff + store submission
4. **Sprint 3 DoD** — added explicit Stripe-prod environment configuration & verification bullet (closes the milestone-vs-DoD gap; carries forward to Sprint 4)
5. **Pre-Launch Smoke disambiguation** — renamed Sprint 4's June 19 task to "Pre-Launch Staging Smoke" (staging/pre-prod) to disambiguate from Launch Day's production Smoke Test on June 22

---

## Track 3 — Sprint Calendar Drift Check

Top-of-document Sprint Calendar cross-checked against detailed sprint sections. No drift detected after Track 1 + Track 2 fixes applied. Themes, date ranges, and goal phrasing are consistent between summary and detail views.

---

## Follow-up Correction Pass — Timeline, Coverage & Smoke Tests

**Date:** May 20, 2026

**Applied corrections:**
- Timeline: clarified June 16 as release-candidate store submission and app-store-affecting mobile code freeze; moved store review into Sprint 4/pre-launch rather than Launch section; added internal/beta fallback for vendor-facing soft launch if public store approval slips; added weekend-monitoring exception for PM only; aligned Sprint 2 App Store creative deliverables and June 19 UAT triage buffer.
- Coverage/mapping: added FR-036 as topline-only A-09d Admin Profile & Settings pending its dedicated PRD; corrected FR-026 misuse for deposit/quote expiry; changed FR-007b installment range to 2-9; reframed FR-002 as V1 head-scan photo set rather than V2 3D; added provider-side FR-008 travel surfaces; added patient/provider FR-019 promotion surfaces; added provider Help Centre/support and admin Help Centre content management; corrected FR-033 ownership away from A-10.
- DoD alignment: added patient final-balance-before-check-in gating; changed payout automation to approval-first processing; made reviews immediate-publication with post-publication moderation; added FR-014 recurring exports and 7-day re-download; removed unsupported DSR export wording; corrected FR-022 provider labels and patient quote-comparison filtering.
- Smoke tests: expanded launch smoke from five isolated flows to eight cross-tenant flows covering inquiry/provider selection, final payment before treatment check-in, travel, aftercare, messaging/admin monitoring, support lifecycle, promotions/affiliate attribution, and compliance/i18n/search.

---

## Structural Change — Modules Table Restructure

All four sprints' Modules sections converted from prose to a 3-column table:

| Tenant | Modules | FR(s) directly affected |

**Rationale:** Module codes (P-XX, PR-XX, A-XX, S-XX) sometimes span multiple sprints, which can mislead testing scope. The FR column is now the authoritative scope marker. Allocation rule applied: **FRs are not split across sprints, except by tenant** (different tenants implementing the same FR can be in different sprints).

**Row counts:** Sprint 1 = 13, Sprint 2 = 8, Sprint 3 = 9, Sprint 4 = 11.

---

## Orphan FR Allocation

Three FRs that were unallocated in the prior plan version are now placed:

- **FR-013 Reviews & Ratings** → Sprint 3 (P-02/PR-06 surfaces + A-01 moderation)
- **FR-021 Multi-Language & Localization** → Sprint 4 (P-01, PR-06, A-09c Part 3 authoring, A-01 surfaces)
- **FR-022 Search & Filtering** → Sprint 4 cross-cutting (P1 MVP scope for provider + admin list views; patient provider-discovery deferred to P2)

---

## Source Documents

- `local-docs/product-plans/2026-05-13/launch-plan.md` — patched in place
- `local-docs/project-requirements/functional-requirements/` — all 36 FRs cross-checked
- `local-docs/project-requirements/update-logs/2026-05-20/LAUNCH_PLAN_PATCH_2026-05-20.md` — earlier same-day patch (timeline shift + aftercare move + initial user stories)
