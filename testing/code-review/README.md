# Code Review (Code vs PRD Conformance)

Static, evidence-based reviews of the source code in `main/` (backend and provider/admin
dashboards) against the FR PRDs, per launch-plan phase. They catch defects manual testing
cannot see: fixture or hard-coded data, missing authorization or provider isolation, broken
state transitions, dashboard/API contract mismatches, and unbuilt PRD branches. The patient
mobile app source is out of scope; patient behavior is reviewed through backend endpoints.

| Item | Value |
|---|---|
| Owning skill | `code-review-conformance` (user-triggered) |
| Consumer skill | `create-bug-tasks` takes only gaps with Status `Confirmed`; `Needs runtime` and `Needs decision` gaps are skipped |
| Location | `<YYYY-MM-DD>/code-review-v<plan>-<phase>-<scope>.md` |
| Example | `2026-10-21/code-review-v2-phase-1-pr-02-fr-004.md` |
| Scope token | `all` (whole phase), lowercase module (`pr-02`), or module plus FR (`pr-02-fr-004`); a repeat run on the same date adds `-r2` |

Each document has a header (run date, repo commits, units planned vs done, staging writes), a
Summary coverage table (Phase › Module › FR › Unit), a gaps-only body with a "Phase exit gates"
section, an Evidence appendix, and unresolved questions. Files here are written only by the
skill; do not edit them by hand except to annotate decisions in Unresolved questions.
