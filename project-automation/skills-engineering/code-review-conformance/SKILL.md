---
name: code-review-conformance
description: Unattended, evidence-based review of the Hairline source code in main/ (Laravel backend + React provider/admin dashboards) against the FR PRDs for one launch-plan phase, one module, or one FR. Derives a frozen list of review units from each PRD (use cases, user stories, main/alternative flows, edge cases, uncovered dashboard screens, phase exit-gate invariants), runs one fresh checker subagent per unit and one refuting verifier per reported gap, and writes a gaps-only hierarchical report under testing/code-review/ that create-bug-tasks can ingest. User-triggered only, never auto-fire. Use it whenever the user explicitly asks to "code review against the PRD", "check conformance", "find code gaps for Phase 1 / PR-02 / FR-004", "audit the code for fixtures, RBAC, provider isolation", to resume such a run, to re-check an existing report after PRD or code changes (Delta mode, "re-run the review", "what changed since the last review"), or to have an independent jury re-judge a report's passing units or gaps (Jury mode). Not for progress percentages (check-progress), PRD-vs-PRD consistency (verify-fr), drafting Plane bug tasks (create-bug-tasks consumes this report), or executing registered tests (web-e2e-*, api-testing, api-flow-testing).
---

# Code Review Conformance

## Purpose

Manual testing exercises the UI with test data, so it cannot see defects that live in code:
hardcoded or fixture data, missing authorization checks, broken state transitions,
API/dashboard contract mismatches, unbuilt PRD branches, untested screens. This skill reviews
the code itself against the FR PRDs, per launch-plan phase, and produces a report whose
Confirmed gaps feed `create-bug-tasks`. Writing automated tests is a non-goal.

The run is long and unattended. Everything that needs a human is asked up front in preflight;
after that the run never stops to ask, so the user can walk away.

## Inputs

- **Plan version**: default `local-docs/product-plans/v2/plan.md` (the current version). Accept
  `v<N>` to use another version.
- **Scope** (one of): a whole phase (`Phase 1`), one module within a phase (`PR-02`), or one FR
  (`FR-004`, optionally with its module). If missing, resolve it in the scope question.
- **Resume**: a path to an existing report under `testing/code-review/` (see Resume mode).
- **Delta**: an existing complete report plus "re-run", "re-check", or "update" (see Delta mode).
- **Jury**: an existing report plus "jury", "second opinion", or "re-verify" (see Jury mode).

All paths below are relative to the workspace root (the folder that contains `local-docs/` and
`main/`).

## Hard rules

These are absolute because breaking any of them corrupts data, leaks secrets, or defeats the
unattended design:

- **Never edit anything in `main/`.** It is the dev team's source; this skill only reads it.
- **Never read `main/hairline-app/`** (Flutter mobile source), not even to locate something.
  Patient-side behavior is checked through backend endpoints only.
- **Never block after preflight.** Once the last preflight question is answered, do not call
  AskUserQuestion again. Log every ambiguity or judgment call as a "Needs decision" gap.
- **One question per AskUserQuestion call.** Ask the preflight questions one at a time, in order.
- **Concurrency only with explicit preflight approval.** Without it, run one subagent at a time.
- **The user picks the engine and model** for checkers, verifiers, and jurors in preflight,
  every run and every mode. Claude subagents are always `subagent_type: "code-reviewer"` with
  the chosen `model` passed explicitly, never `general-purpose` and never the session default.
- **No MCP, ToolSearch, or skill calls by default** in any subagent. They are allowed only when
  a finding needs evidence that source reading and a direct HTTP request cannot give.
- **External engines (Codex, OpenCode) run read-only and credential-blind**, with probes off,
  and only after their canary passes (`references/subagent-engines.md`).
- **Never print tokens, passwords, or credential values** into the report, the tracker, or chat.

Other boundaries (non-goals): no Plane task creation, no edits to `progress-tracking/` or
`check-progress` rows, no automated test writing, no files other than the one report (the update
log is written by whoever runs the session, per project rules).

## Why the run is shaped this way

- **Fresh checker per unit** keeps each check focused on one PRD slice and prevents shortcut
  behavior: a checker that knows there are 140 units left, or sees earlier verdicts, tends to
  skim or pattern-match. Checkers therefore never see the unit count or other results. Time is
  not a constraint; quality is.
- **Refuting verifier per gap** exists because static review produces false positives (logic
  in a job, middleware, another repo, a policy class). A gap survives only if a second, fresh
  agent tried to disprove it and could not.
- **Code is the truth, code maps are a locator.** `project-notes/code-map-*.md` tell you where
  to start, but code changes faster than the maps. Every finding is confirmed in `main/` source.
- **Main agent is the sole writer** and writes as results arrive, so a crash loses at most the
  in-flight units, and the report plus tracker are enough to resume.

## References (load when the step says so)

| File | Load at |
|---|---|
| `references/item-derivation.md` | Step 2, before deriving units |
| `references/rubric.md` | Step 2 (to brief yourself) and Step 6 (to finalize verdicts) |
| `references/output-structure.md` | Step 4, before writing the skeleton |
| `references/checker-brief.md` | Step 5, copied verbatim into each checker prompt |
| `references/verifier-brief.md` | Step 6, copied verbatim into each verifier prompt |
| `references/subagent-engines.md` | Step 3 (engine question) and before the first spawn |
| `references/delta-mode.md` | Delta mode, before anything else |
| `references/jury-mode.md` | Jury mode, before anything else (holds the juror brief) |

## Workflow

### 1. Preflight: resolve plan, phase, modules, FRs

1. `CURRENT_DATE=$(date +%Y-%m-%d)`.
2. Resolve the plan file. Read only its "Recommended four-phase release roadmap" section and the
   two module status tables (Provider / Admin) that give each module's "FR focus".
3. Resolve the phase from the scope (a module or FR maps to the earliest phase that lists it;
   if it appears in several phases, carry that into the scope question).
4. Build the in-scope tree: Phase › Module › FR. Phase rows sometimes name a partial module
   ("essential PR-06 profile/pricing", "A-01 inquiry/quote oversight"); propose the FRs that
   match the wording and let the scope question confirm them.
5. Locate each FR PRD: `local-docs/project-requirements/functional-requirements/frNNN-*/prd.md`.
6. Read the code maps that the scope needs (`local-docs/project-notes/code-map-backend.md` and
   `code-map-frontend.md` only; never the app map's targets) and note, per FR, the folder groups
   and entry-point files. These become each checker's "code-map pointers".
7. Record repo SHAs:
   `git -C main/hairline-backend rev-parse --short HEAD` and
   `git -C main/hairline-frontend rev-parse --short HEAD`.
8. Resolve the probe environment: the backend base URL from the phase test guide
   (`local-docs/testing/manual/v<N>/phases/<phase>/test-guide.md`, section "Test Environment and
   Accounts") and the Postman collection/environment IDs from
   `local-docs/testing/automated/api/endpoints/collection-map.md` ("Connection Details"). Note the
   credential files that exist in `local-docs/testing/test-data/credentials/` by name only.

### 2. Derive the review units

Load `references/item-derivation.md` and follow it exactly: it fixes the section order, unit
types, ID scheme, screen dedupe, exit-gate units, and how granular rules fold into parents. Read
each PRD by section (list anchors with `rg -n "^#{2,4} " <prd.md>`, then range-read); many PRDs
exceed 1000 lines and must never be read whole.

For each unit, keep: unit ID, title, unit type, Phase › Module › FR placement, PRD line range(s)
of its excerpt, folded check points, and code-map pointers. This list stays in your context and
the report skeleton; it is not written to any other repo file.

### 3. Approval gate (AskUserQuestion, one question per call, in this order)

1. **Scope**: confirm Phase › Module › FR tree, including the FRs chosen for partial modules.
2. **Frozen unit list + count**: show the count per FR and per unit type and the total, plus
   where the full list will appear (the report Summary). Approval freezes the list. If the user
   asks for changes, re-derive and re-ask this question only.
3. **Engine and model**: load `references/subagent-engines.md` and offer its options: Claude
   `code-reviewer` on Sonnet (mark it Recommended), Haiku (cheapest; warn it raises more false
   positives, each costing a verifier), or Opus (highest cost); Codex headless; OpenCode
   headless. Allow different choices for checkers and verifiers in free text. When an external
   engine is chosen, the question also asks which Claude model to fall back to if its canary
   fails, and states that probes and staging writes are off for that engine.
4. **Concurrency**: off (one subagent at a time) or on with a cap (suggest 3, allow up to 4).
   Approval explicitly overrides the project's subagent-limit rule for this run only.
5. **Probes and staging writes**: probes off, read-only probes, or probes with staging writes.
   State the target base URL in the question so the user can catch a production host. Writes
   are allowed only if approved here. Skip this question when every role runs on an external
   engine (probes are off for them).

If the user declines the scope or the list entirely, stop without writing a report. After
the last question, the run proceeds to the end without asking anything else.

### 4. Create the tracker and the report skeleton

1. Create one tracker task per frozen unit (TaskCreate), subject = unit ID + title, in the
   derivation order. State the count in the first task's description. The tracker is the live
   work queue; it lives only in the harness, never in a repo file.
2. Load `references/output-structure.md`. Create
   `local-docs/testing/code-review/<CURRENT_DATE>/code-review-v<plan>-<phase>-<scope>.md` with
   the header (including the Engine and Revisions lines), a Summary row for every frozen unit
   with verdict `Pending`, empty body sections for each Phase › Module › FR, the "Phase exit
   gates" section, the Evidence appendix, the unresolved-questions section, and an empty Unit
   baseline table. If a report for the same scope already exists, the request is a Delta run:
   switch to Delta mode instead of writing a second file.
3. If an external engine was chosen, run its canary now (`references/subagent-engines.md`). On
   failure, switch to the approved fallback and note it under Unresolved questions as a method
   deviation.

### 5. Checker loop

For each tracker task in order (or up to the approved cap in parallel):

1. Mark the task in progress.
2. Spawn a **fresh** checker on the approved engine: for Claude, the Agent tool with
   `subagent_type: "code-reviewer"` and the approved `model`, prompt starting with the override
   line from `references/subagent-engines.md`; for Codex or OpenCode, the Bash command given
   there. Its prompt contains only:
   - the full text of `references/checker-brief.md`, with the run's probe settings filled in
     (probes on/off, writes on/off, base URL, collection and environment IDs, credentials
     folder path; for an external engine probes are `off` and the credentials path is omitted),
     followed by the full text of `references/rubric.md` (the verdict and severity rubric);
   - the unit block: ID, title, type, FR, module, tenant, check points;
   - the PRD excerpt for this unit (the exact lines, pasted; include the PRD path and line
     range so the checker can cite sections);
   - the code-map pointers for this FR.
   Never include the unit count, the list of other units, or any other result.
3. Validate the return against the schema in the brief. If it is malformed, send one follow-up
   to the same subagent asking it to re-emit in the schema. If that fails, or the subagent
   errors or times out, record the unit as `Not checked — <reason>`.
4. If the return has no gaps, update the unit's Summary row immediately and complete the task.
5. If it has gaps, go to Step 6 for each gap before completing the task.

With concurrency on, keep at most `cap` subagents in flight (checkers and verifiers combined)
and process returns in arrival order. You remain the only writer to the report, so edits never
collide.

### 6. Verifier per gap, then write immediately

For each gap a checker reported (including those it tagged Needs runtime or Needs decision):

1. Spawn a **fresh** verifier on the approved verifier engine and model (same mechanics as
   Step 5.2) with `references/verifier-brief.md` verbatim (probe
   settings filled, rubric appended), the gap (claim, PRD ref, evidence), the unit block, the unit's PRD excerpt, and the code-map pointers. Do not include
   the checker's other gaps or any other unit.
2. Apply the verifier outcome using `references/rubric.md`:
   - **Confirmed**: keep the gap; status as the checker tagged it (Confirmed, Needs runtime, or
     Needs decision).
   - **Downgraded**: keep the gap with the lower severity or the weaker status the verifier
     gives, and note the reason in the Evidence appendix.
   - **Refuted**: drop the gap from the body; add one line to "Refuted findings" in the Evidence
     appendix with the verifier's counter-evidence.
   - Verifier failure: keep the gap with status `Needs runtime` and note "verifier did not
     complete" in the Evidence appendix; never promote an unverified gap to Confirmed.
3. As soon as all gaps for the unit are settled, insert them under the unit's heading in the
   body, add evidence and probe lines to the appendix, append any staging writes to the header's
   write log, finalize the unit verdict, update its Summary row, add its Unit baseline row
   (excerpt hash and cited files, see `references/output-structure.md`), and complete the
   tracker task. Do not wait for other units.

### 7. Reconcile planned vs done

When the tracker has no pending tasks:

1. Count Summary rows: every frozen unit must have a final verdict (no `Pending`). Units that
   could not be checked appear as `Not checked — <reason>`; they count as done-but-not-checked,
   never as silently dropped.
2. Fill the header line `Units planned / checked / not checked`. Planned must equal
   checked + not checked. If it does not, find the missing unit and record it as Not checked
   with the reason "missing from run".
3. Confirm every Confirmed gap has a file:line pointer and a PRD section reference; downgrade
   any that lack them to `Needs runtime` and note why.
4. Collect "Needs decision" items and open issues into the unresolved-questions section.

### 8. Final summary (chat)

Return: report path, engine and model used, units planned/checked/not checked, gap counts by
status and severity, staging writes made (count), notable map drift, and the next step (for example: "run
create-bug-tasks on the Confirmed gaps in <report>"). Keep it short; the report holds detail.

## Resume mode

Use when the user points at an existing report or asks to resume a crashed run.

1. Read the report header (scope, plan version, approvals, SHAs) and the Summary table.
2. Units with a final verdict are done. Units still `Pending` form the remaining queue.
   If the user asks, also re-queue `Not checked` units.
3. Ask, one AskUserQuestion per call: (a) confirm the resume (remaining count, and whether the
   earlier concurrency and probe/staging-write approvals still apply); (b) the engine and model
   for the remaining units (show what the header recorded; the user may change it, and a
   change is logged on the Resumed line). This counts as the run's preflight; after it, never
   block.
4. If the current repo SHAs differ from the header, record the new SHAs on a "Resumed" header
   line so readers know later units ran against newer code.
5. Re-derive only the remaining units' PRD excerpts and pointers (IDs are stable, see
   `references/item-derivation.md`), recreate tracker tasks for them, and continue at Step 5.

## Delta mode

Use when the user asks to re-run, re-check, or update a complete report after the PRDs or the
code changed. Load `references/delta-mode.md` and follow it: it detects new, changed, affected,
renamed, and retired units (PRD excerpt hashes or PRD git history, plus code files changed since
the recorded commits), tags gaps that are in the current deferred backlog as `Deferred
(DEF-nnn)`, shows the delta plan for approval (a dry run stops there), then re-checks only those
units with the normal Steps 5 and 6 and updates the report in place. Gap IDs carry forward and
are never reused; a gap the code now meets becomes `Fixed <date>`, never silently deleted.

## Jury mode

Use when the user wants an independent second judgment over a finished report. Load
`references/jury-mode.md` and follow it: preflight asks what to judge (passing units, open
gaps, or both), the engine (prefer a different model family from the original run),
concurrency, and probes; then one fresh juror per item. The jury annotates only: a `Jury`
column in the Summary and a `## Jury` section with a disagreements list. It never changes an
original verdict, status, or severity; the user settles each disagreement.

## Report consumers

- **create-bug-tasks** reads the body gap tables. Its "confirmed bugs only" rule means it takes
  rows whose Status is `Confirmed` and skips every other status (`Needs runtime`, `Needs
  decision`, `Fixed`, `Retired`, `Deferred`). Module and FR
  come from the section headings; Gap ID becomes its Source Bug ID; Priority maps directly.
  Code gaps have no observed manual repro, so each gap carries PRD-derived "Steps to reproduce"
  and each FR section carries a `PRD source` line; the executor re-reads those PRD sections to
  complete the steps. `create-bug-tasks` itself is not changed.
- **deferred-backlog** records gaps the team chose not to fix now; Delta mode reads its current
  version and never re-raises those gaps.
- **Humans and AI agents** read the Summary first, then jump to one module or FR.
