# Jury Mode

A second, independent judgment over a finished report. Jurors re-examine the units the review
passed, the gaps it reported, or both, ideally on a different engine or model family than the
original run. The jury only annotates: it never changes an original verdict, status, or
severity. Disagreements go to the user to settle.

## Why

A checker and its verifier on the same model can share the same blind spots: a missing
authorization check that both read past, or a gap both confirm because they read the PRD the
same wrong way. A juror from another model family catches those. Passing units get no verifier
on a normal run, so the jury is the only second look they ever get.

## 1. Read the report

Read the header (engine line, scope, latest Revisions), the Summary, and the Evidence entries
for the items in scope. Never read the whole report.

## 2. Preflight (one AskUserQuestion per call, in this order)

1. **What to judge**: passing units only (verdict `Conforms`), open gaps only (`Confirmed`,
   `Needs runtime`, `Needs decision`; never Fixed, Retired, or Deferred), or both. Allow a filter
   in free text (for example "P0 and P1 gaps only" or "PR-02 only"). State each option's item
   count.
2. **Engine and model**: same options as the main workflow. Recommend an engine from a
   different family than the report's checker engine (Codex when the review ran on Claude, and
   the reverse), and say why.
3. **Concurrency**: as in the main workflow.
4. **Probes**: off by default. Allow read-only probes only for a Claude engine and only when the
   user approves; jurors never write to staging.

After question 4, never block.

## 3. Juror per item

One fresh juror per item, never batched. The prompt holds the brief below (placeholders
filled), the rubric, the unit block, the unit's PRD excerpt with path and line range, the
code-map pointers, and the item: for a passing unit, its conforming evidence; for a gap, its row
(Gap ID, priority, status, issue, PRD requires, evidence pointers). Do not include the original
engine, other items, or counts.

Validate the return like a checker return (one re-emit request, then record `Unsure — juror did
not complete`).

## 4. Write (annotate only)

- Add a `Jury` column to the Summary table if it is not there yet (fill `-` for items not
  judged). For a unit, write the juror outcome for the unit and, when its gaps were judged, the
  counts (`Agree; gaps 3 agree / 1 disagree`).
- Add a `## Jury` section just before `## Evidence`, with one row per judged item:

  ```markdown
  ## Jury

  Run <date>, engine <engine, model>, scope <passing units / gaps / both>. Original verdicts are unchanged; the user settles disagreements.

  | Item | Original | Juror | Outcome | Reason | Evidence |
  |---|---|---|---|---|---|
  | FR-004/W3-G1 | Confirmed P1 | Confirmed P1 | Agree | Expiry command absent from scheduler. | hairline-backend/app/Console/Kernel.php:30-48 |

  ### Jury disagreements

  - FR-004/US2 (Conforms → Gap P0): provider can read another provider's quote; policy not applied on show route (hairline-backend/routes/api.php:212). Status: open.
  ```

- A second jury run appends a new `Run <date>` block under `## Jury` rather than replacing the
  first.
- Append the Revisions entry described in `output-structure.md`.

When the user later settles a disagreement, edit only what they decided (for example, add the
new gap with the next unused Gap ID, or change a severity) and change that disagreement's
`Status: open` to `Settled <date>: <decision>`.

## Juror brief (fixed prompt template)

---BEGIN BRIEF---

You are an independent juror. Another reviewer judged whether the Hairline source code meets
ONE part of a functional requirement (FR) PRD. Reach your own judgment from the source and the
PRD, then say whether you agree. Do not defer to the earlier judgment, and do not disagree just
to be different: either way, back your outcome with file:line or a PRD quote.

## What you are judging

- **A passing unit** (the reviewer found it conforms): look for any check point the code does
  not meet, especially authorization and tenant isolation, hard-coded or fixture data, missing
  state transitions, and dashboard calls to endpoints that do not match the backend.
- **A gap** (the reviewer found a defect): decide whether it is real, whether its status is
  right (Confirmed needs file:line and a PRD section), and whether its severity fits the rubric.
  Look for the behavior in the places a static review misses: the other repo, middleware,
  policies, form requests, jobs and scheduled commands, observers, alternate routes.

## Rules

- Repo scope: `{{BACKEND_PATH}}` and `{{FRONTEND_PATH}}` only. Never open or search the mobile
  app source. Never modify any file, and do not run builds, linters, or tests.
- Code is the truth; the code-map pointers are only where to start.
- Search narrowly (`rg -n -m 20 <pattern> <path>`); narrow any search that floods.
- Use no MCP tool, ToolSearch, or skill unless the outcome needs evidence that reading source
  cannot give. Probes for this run: **{{PROBES}}** (off = do not call the API).
- Never output credential values.
- If you cannot decide from source, return `Unsure` with what you would need to decide.

## Return format (exactly this, nothing before or after)

```yaml
item: <unit ID or gap ID>
kind: unit | gap
outcome: Agree | Disagree | Unsure
juror_verdict: <for a unit: Conforms | Partial | Gap | Needs runtime | Needs decision>
juror_status: <for a gap: Confirmed | Needs runtime | Needs decision | Not a gap>
juror_severity: <P0-P3, for a gap, or for a new gap found in a passing unit>
reason: <one or two sentences>
evidence: [<path:line or PRD section>]
searched: [<short list of locations checked>]
```

---END BRIEF---
