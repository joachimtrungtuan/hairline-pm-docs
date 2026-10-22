# Code Review (Code vs PRD Conformance)

Static, evidence-based reviews of the source code in `main/` (backend and provider/admin
dashboards) against the FR PRDs, per launch-plan phase. They catch defects manual testing
cannot see: fixture or hard-coded data, missing authorization or provider isolation, broken
state transitions, dashboard/API contract mismatches, and unbuilt PRD branches. The patient
mobile app source is out of scope; patient behavior is reviewed through backend endpoints.

| Item | Value |
|---|---|
| Owning skill | `code-review-conformance` (user-triggered) |
| Consumer skill | `create-bug-tasks` takes only gaps with Status `Confirmed`; every other status (`Needs runtime`, `Needs decision`, `Fixed`, `Retired`, `Deferred`) is skipped |
| Deferred gaps | Recorded in `local-docs/deferred-backlog/` by the `deferred-backlog` skill; Delta runs tag them `Deferred (DEF-nnn)` and never re-raise them |
| Location | `<YYYY-MM-DD>/code-review-v<plan>-<phase>-<scope>.md` |
| Example | `2026-10-21/code-review-v2-phase-1-pr-02-fr-004.md` |
| Scope token | `all` (whole phase), lowercase module (`pr-02`), or module plus FR (`pr-02-fr-004`). One report per scope: a later re-check is a Delta run that updates the report in place |

Each document has a header (run date, repo commits, engine and model, units planned vs done,
staging writes, revisions), a Summary coverage table (Phase › Module › FR › Unit), a gaps-only
body with a "Phase exit gates" section, an Evidence appendix, unresolved questions, and a Unit
baseline (PRD excerpt hash and cited files per unit, used by Delta runs). A Jury run adds a
`Jury` column to the Summary and a `## Jury` section with disagreements for the user to settle;
it never changes original verdicts. Files here are written only by the
skill; do not edit them by hand except to annotate decisions in Unresolved questions.
