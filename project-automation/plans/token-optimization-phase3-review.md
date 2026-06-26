# Token Optimization — Phase 3 Review Playbook

**Status**: ⏳ Pending (trigger not yet met)
**Created**: 2026-06-26
**Owner**: whoever picks it up — any agent or the user
**Applies to**: all AI agents/tools in this project (Claude Code, Codex, Cursor, Antigravity, …)

> **How to resume:** open this file, confirm the trigger below is met, run the measurement,
> fill the Results Log, then apply the Decision Rubric. No need to reload prior chat history —
> everything needed is here. This file *is* the handoff.

---

## What this is

Phases 1–2 changed how agents navigate and read this repo to cut token burn (see
`local-docs/project-requirements/update-logs/2026-06-26/`). Phase 3 is **not build work** —
it is a measurement checkpoint to confirm the changes actually reduced burn without hurting
work quality, and to spot which rule (if any) is being ignored.

## Trigger (start Phase 3 when ALL are true)

- [ ] At least **3–5 real working sessions** have been completed *under the new rules*
      (i.e. agents started at `local-docs/INDEX.md`, used capped search, read by section).
- [ ] Those sessions cover a mix of task types (e.g. PRD read/edit, FR verify, task creation,
      Plane work) so the comparison isn't skewed to one workflow.

## Baseline to beat (from the pre-change analysis of 19 rollout sessions)

The headline 99.9M cumulative was mostly **cached** input — track the painful, controllable
numbers instead:

| Metric (pre-change) | Value |
|---|---|
| Uncached input tokens | ~10.7M |
| Assistant output tokens | ~505k |
| `rg`/search tool-output tokens | **~2.79M** (largest controllable burn) |
| File-read / doc-slice tokens | ~1.13M |
| `git diff` inspection tokens | ~262k |
| Worst single session | 16.19M cumulative |
| FR-018 Plane-task session | 4.69M cumulative |

## Per-phase targets (the rules were designed to hit these)

| Phase | Target |
|---|---|
| Recon | ≤ 20k tokens |
| Source read | ≤ 40k |
| Edit | ≤ 30k |
| Verify | ≤ 20k |
| Full feature workflow | < 150k–250k (not millions) |

**Primary KPI**: uncached input + tool-output tokens per phase. Ignore the cached-input
headline — it is heavily discounted and misleading.

## What to measure

For each reviewed session, capture:

1. Total tokens, and the split: cached input / uncached input / output.
2. Tool-output tokens, broken out by `rg`/search vs file reads vs `git`.
3. Largest single tool call (the worst offender).
4. Behavior checks (qualitative): Did it start at INDEX? Any project-wide `rg -n`? Any
   full reads of ⚠️ >1000-line files? Any unsolicited update-log / `git diff` reads?
   Was work split into fresh threads at phase boundaries?

### How to pull the numbers (tool-specific)

- **Codex**: have it analyze its own session logs (the original baseline was produced this
  way) — sum input/cached/uncached/output and bucket tool outputs by command.
- **Claude Code**: use session/usage data for the same buckets; `/context` and transcript
  inspection for per-call sizes.
- **Any tool**: at minimum, eyeball the largest tool outputs and confirm no single search
  dumped thousands of lines (the `search.sh` wrapper should have prevented this).

## Decision rubric

- **Pass** (uncached + tool-output down materially vs baseline, per-phase targets roughly
  met, quality unaffected): keep the regime as-is; record the win.
- **Partial** (some improvement, one rule routinely skipped): identify the rule, sharpen its
  wording in `CLAUDE.md`/`AGENTS.md`, or make it *hard* (e.g. mandate `search.sh`, add the
  Phase 4 validator). Re-measure.
- **Fail** (no improvement): diagnose whether the rules aren't being followed (enforcement
  problem) or aren't sufficient (design problem) before changing anything.

## Results Log (fill on review)

| Date | Sessions reviewed | Uncached in | Output | Search out | Largest call | Targets met? | Verdict | Notes |
|---|---|---|---|---|---|---|---|---|
| *pending* | | | | | | | | |

## After Phase 3

- If Pass → consider whether Phase 4 (doc/artifact validator) is still worth building.
- Always log the review outcome under `update-logs/` per the Update Log Protocol.
