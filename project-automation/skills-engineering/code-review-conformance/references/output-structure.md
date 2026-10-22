# Output Structure

Exact structure of the code review document this skill writes. Keep it concise but detailed,
readable by humans and AI agents, with no sections beyond these.

**Path**: `local-docs/testing/code-review/<YYYY-MM-DD>/code-review-v<plan>-<phase>-<scope>.md`

- `<plan>`: plan version number (`2`).
- `<phase>`: `phase-<n>` (`phase-1`).
- `<scope>`: `all` for a whole phase, the lowercase module (`pr-02`), or module plus FR
  (`pr-02-fr-004`).
- Example: `testing/code-review/2026-10-21/code-review-v2-phase-1-pr-02-fr-004.md`.
- One report per scope. A later re-check of the same scope is a Delta run that updates the
  latest report in place (see `delta-mode.md`); it never creates a second file. A new file is
  written only for a fresh full run, which goes under its own run-date folder.

**Markdown rule**: never put a literal pipe character inside a table cell (it breaks the
column). Use `/`, commas, `and`, or `<br>` instead. This matters most in Issue and Evidence
cells.

## Skeleton (written at Step 4, before any checker runs)

```markdown
# Code Review: v<plan> <Phase name> — <scope label>

**Run date**: YYYY-MM-DD
**Plan**: local-docs/product-plans/v<plan>/plan.md, <Phase n — name>
**Scope**: <Phase › Module › FR tree, one line>
**Repo commits**: hairline-backend `<sha>`, hairline-frontend `<sha>`
**Approvals**: concurrency <off / on, cap n>; probes <on / off>; staging writes <off / on> (target <base URL>)
**Engine**: checkers <engine, model>; verifiers <engine, model>; fallback <engine, model or none>
**Units planned / checked / not checked**: <N> / <pending> / <pending>
**Staging writes made**: none
**Run state**: In progress
**Revisions**: none

## Summary

| Phase | Module | FR | Unit | Verdict | Gaps (Confirmed / other) |
|---|---|---|---|---|---|
| P1 | PR-02 | FR-004 | FR-004/W1 Provider quote creation | Pending | - |
| P1 | Exit gate | - | P1-GATE/provider-isolation | Pending | - |

## Phase 1 — <phase name>

### PR-02 — <module name>

#### FR-004 — <FR title>

## Phase exit gates

## Evidence

### Pointers and probes

### Refuted findings

### Map drift

## Unresolved questions

## Unit baseline
```

Every frozen unit gets one Summary row in derivation order; the Summary doubles as the coverage
table and the resume checkpoint.

## Filling the body (Step 6)

Only units with at least one surviving gap get a heading in the body. Units that conform (or are
Not checked) appear only in the Summary.

```markdown
##### FR-004/W3 — Quote Expiry & Status Transitions

PRD source: local-docs/project-requirements/functional-requirements/fr004-.../prd.md (re-read the cited sections before acting on these gaps)

| Gap ID | Priority | Status | Issue | PRD requires | Steps to reproduce (from PRD) | Direction to comply | Evidence |
|---|---|---|---|---|---|---|---|
| FR-004/W3-G1 | P1 | Confirmed | Expired quotes keep status "sent"; no job changes them. | Quote auto-expires and status updates at expiry (§Workflow 3 step 2) | 1. As a provider, send a quote with a short expiry (§Workflow 3 step 1).<br>2. Wait past the expiry time.<br>3. Open the quote: PRD expects status "expired". | Expire quotes at the configured time and notify the provider. | E-12, E-13 |
| FR-004/W3-G2 | P2 | Needs runtime | Expiry notification may not dispatch; listener binding is config-driven. | Provider notified on expiry (§Business Rules 7) | Follow §Workflow 3 steps 1 to 2, then check the provider's notifications (§Business Rules 7). | Confirm the notification is sent on expiry. | E-14 |
```

Under each `####` FR heading, write one `PRD source:` line with the PRD path and the instruction
to re-read the cited sections, so whoever acts on a gap (a human, `create-bug-tasks`, or a
developer) checks the requirement in the PRD rather than relying on this summary.

Field rules:

- **Gap ID**: `<unit ID>-G<n>`; stable within the document.
- **Priority**: P0 to P3 from `rubric.md`.
- **Status**: `Confirmed`, `Needs runtime`, or `Needs decision` on a first run. Delta mode may
  also set `Fixed <date>`, `Retired <date>`, or `Deferred (DEF-nnn)`; those rows stay in the
  table for history and are skipped by `create-bug-tasks`.
- **Issue**: what is wrong, in observable terms (this is the actual outcome).
- **PRD requires**: the expected outcome with the PRD section reference in parentheses.
- **Steps to reproduce (from PRD)**: the user-facing steps that expose the gap, taken from the
  PRD flow the unit covers (actor, action, expected result), each step citing its PRD section.
  Use `<br>` between steps. Code gaps have no recorded manual repro, so these steps are derived
  from the PRD, not observed; when the PRD flow is too long to restate, write the actor and the
  start and end steps and say "re-read <PRD section>".
- **Direction to comply**: one sentence, behavior terms, no implementation prescription.
- **Evidence**: IDs of Evidence appendix entries (`E-n`); every Confirmed gap must point to at
  least one file:line entry.

Exit-gate units use the same table under `## Phase exit gates`, with a `##### P1-GATE/<slug>`
heading per gate that has gaps.

## Evidence appendix

```markdown
### Pointers and probes

- E-12 (FR-004/W3-G1): main/hairline-backend/app/Console/Kernel.php:30-48, no quote expiry command scheduled
- E-13 (FR-004/W3-G1): PRB GET /provider/quotes/{id} as V1, 200, status "sent" past expiry
- E-14 (FR-004/W3-G2): main/hairline-backend/app/Providers/EventServiceProvider.php:55

### Refuted findings

- FR-004/A2-G1: refuted, draft archive handled by ArchiveDraftQuotes job (main/hairline-backend/app/Jobs/ArchiveDraftQuotes.php:20)

### Map drift

- code-map-frontend.md names src/pages/quotes/; source moved to src/features/quotes/
```

Staging writes, when approved and made, are counted in the header line
`**Staging writes made**: <n> (see E-...)` and each write has its own Evidence entry marked
`WRITE`. Never include tokens, passwords, or credential values; name accounts by row ID only.

## Unresolved questions

Bullet list at the end: every `Needs decision` gap (by Gap ID, one line each) and any run-level
open issue (for example, units Not checked and why, or a PRD conflict spanning several units).

## Unit baseline (Step 6, one row per unit as it completes)

The last section of the report. Delta mode uses it to tell which units changed since this run,
so it records what each verdict was based on.

```markdown
| Unit | PRD lines | Excerpt hash | Cited files |
|---|---|---|---|
| FR-004/W3 | 210-248 | 3f9a1c0b7d2e | hairline-backend/app/Console/Kernel.php, hairline-backend/app/Providers/EventServiceProvider.php |
```

- **PRD lines**: the excerpt range used for this run (it may shift later; the hash is what is
  compared).
- **Excerpt hash**: first 12 characters of the SHA-256 of the excerpt with trailing whitespace
  stripped from each line (command in `delta-mode.md`).
- **Cited files**: repo-relative file paths (no line numbers) from the unit's gap evidence and
  conforming evidence, comma-separated. Delta mode re-checks the unit when any of them changes.

## Revisions line (Delta and Jury mode)

Each Delta or Jury run appends one entry to the `**Revisions**` header line, separated by `;`:
`<date> delta — repo commits <backend sha>, <frontend sha>; deferred backlog <vNN file>;
re-checked <n>, fixed <n>, retired <n>, new gaps <n>` or `<date> jury — scope <units / gaps /
both>, engine <engine, model>; agree <n>, disagree <n>, unsure <n>`.

## Final header update (Step 7)

Set `Units planned / checked / not checked` with real counts (planned must equal checked plus
not checked), `Staging writes made`, and `Run state: Complete` (add a `Resumed <date>, repo
commits <shas>` line when resumed).

## How create-bug-tasks reads this document

| Element | create-bug-tasks field |
|---|---|
| `###` module heading | Product Module |
| `####` FR heading | FR |
| `#####` unit heading | Flow / Story |
| Gap ID | Bug ID (Source Bug ID) |
| Priority | Priority |
| Issue | Issue and Actual Outcome |
| PRD requires | Expected Outcome |
| Steps to reproduce (from PRD) | Steps to Reproduce (the executor re-reads the `PRD source` sections to complete or confirm them) |
| Direction to comply | Notes |
| Evidence (resolved via appendix) | Evidence |
| Status | Only `Confirmed` rows are confirmed bugs; `Needs runtime` and `Needs decision` rows are skipped |
