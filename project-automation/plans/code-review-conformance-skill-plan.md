# Code Review Conformance Skill — Confirmed Brief

Status: approved by user 2026-10-21 (advisory session). This file is the durable record of the
user's intent; the skill must stay faithful to it.

## Why

Manual testing (testing/manual/v<N>/phases/) exercises the UI with test data. It cannot see
defects that live in code: hardcoded/fixture data, missing authorization checks, broken state
transitions, API/dashboard contract mismatches, unbuilt PRD branches, untested screens. We need
an unattended, evidence-based review of the code against the PRDs, per launch-plan phase, whose
report can feed the existing `create-bug-tasks` skill. Writing a full automated test suite is a
non-goal (too costly, drifts from PRDs).

## Requirements

1. **Preflight** resolves the plan version (currently `product-plans/v2/plan.md`), the phase, and
   the modules/FRs in scope. Run scope may be a whole phase, one module, or one FR.
2. **Item derivation** from each in-scope FR PRD: one item per use case, user story / user
   scenario, main flow, alternative flow, and edge case; plus one item per provider/admin
   dashboard screen not already covered by a flow item; plus one item per phase exit-gate
   invariant from the plan (RBAC, provider isolation, no fixtures, privacy, etc.). Granular
   business/security/validation rules are NOT separate items — they become check points inside
   their parent item. Stable unit IDs (e.g. `FR-004/A2`, `FR-004/SCR-quote-detail`).
3. **Task list** lives in the harness task tracker (TaskCreate/TaskUpdate), never in a repo
   file. It is frozen after preflight confirmation with the count stated. The report carries the
   coverage table; at the end, planned count must reconcile with completed count.
4. **Approvals**: all decisions via AskUserQuestion, one question per call, front-loaded in
   preflight: (a) scope, (b) frozen item list + count, (c) concurrency on/off + cap,
   (d) staging writes on/off. After preflight the run NEVER blocks; ambiguities/judgment calls
   are logged in the report as "Needs decision".
5. **One fresh checker subagent per item.** It receives only: fixed checker brief, that unit's
   PRD excerpt, code-map pointers, probe rules. It does not see the item count or other results
   (prevents shortcut/bias behaviour). Quality over speed; time is not a constraint.
6. **Code scope**: `main/hairline-backend/` in full (including patient API endpoints the mobile
   app calls) and `main/hairline-frontend/` (provider + admin dashboards). `main/hairline-app/`
   (Flutter mobile source) is excluded — never read. Patient endpoints are found via backend
   routes, system-technical-spec, and the Postman collection.
7. **Source of truth is the code, not the code map.** Code maps (`project-notes/code-map-*.md`)
   are a locator/reference only; code changes faster than the maps are refreshed. Every finding
   must be confirmed in the actual source in `main/`; a map/code disagreement is noted, never
   trusted over source.
8. **Runtime probes** allowed via Postman MCP / collection or direct HTTP requests to staging,
   using test accounts in `testing/test-data/credentials/`. Read-only by default; writes only if
   approved for this run in preflight, and every write is logged in the report. Never print
   tokens/credentials into reports.
9. **Every gap gets a fresh verifier subagent** that tries to refute it. Survivors are
   "Confirmed"; refuted ones get one line in the Evidence appendix.
10. **Write immediately**: main agent is the sole writer; it writes the report skeleton at
    preflight and inserts each result under its unit as soon as it arrives (no waiting for all
    agents). Skeleton + tracker enable resume after a crash.
11. **Concurrency** only with explicit preflight approval, which overrides the project's
    subagent-limit rule for that run. Suggested default cap 3–4.
12. **Subagent return contract**: fixed, compact structure (unit ID, verdict, gaps with severity,
    PRD ref, file:line evidence, probe calls) so hundreds of returns do not flood the main
    context.

## Report

- Path: `testing/code-review/<YYYY-MM-DD>/code-review-v<plan>-<phase>-<scope>.md`
  (date folder; filename reflects the work; not grouped by plan-version folder).
- Header: run date, repo commit SHAs, items planned vs done, staging writes made.
- **Summary**: short coverage table of everything checked, hierarchy Phase › Module › FR › Unit,
  verdict + gap count.
- **Body**: sections Phase › Module › FR › Unit, plus a "Phase exit gates" section; lists ONLY
  gaps (units without gaps appear only in the summary). Each gap: ID, severity, status
  (Confirmed / Needs runtime / Needs decision), what is wrong, what the PRD requires (section
  ref), steps to reproduce derived from the PRD flow, direction to comply, evidence pointer.
  Each FR section names its PRD source and tells the executor to re-read the cited sections
  (`create-bug-tasks` itself is not changed).
- **Evidence** appendix at the end: file:line pointers, probe calls, refuted findings.
- Concise but detailed; usable by humans and AI agents; no unnecessary sections.
- Must be consumable by `create-bug-tasks`: only "Confirmed" gaps are bugs; "Needs runtime" /
  "Needs decision" are tagged so that skill skips them.

## Non-goals

Writing automated tests; editing `main/`; reading `hairline-app/` source; Plane task creation;
updating `progress-tracking/` or `check-progress` rows (progress % stays with `check-progress`).

## Rollout

Pilot on one Phase 1 PR-02 FR → human review of every finding → tune briefs → one full module →
full phase.

## Success metrics

Planned = completed in every report; 100% of Confirmed gaps have file:line + PRD ref; pilot
false-positive rate < 15%; `create-bug-tasks` ingests without reformatting; zero reads of
`hairline-app/`.
