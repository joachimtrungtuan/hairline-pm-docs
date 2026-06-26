# Agent Guidelines Restructure + Wayfinder Index + Token Governance

**Date**: 2026-06-26
**Type**: Structural change to project guidelines + new navigation document
**Scope**: `CLAUDE.md`, `AGENTS.md` (root), `local-docs/INDEX.md` (new), `local-docs/README.md`

## Motivation

AI agents (notably Codex) were exhausting token quotas even on lightweight tasks. Analysis of
19 rollout sessions showed the burn is dominated by **input context**, not output: broad
`rg -n` searches (~2.79M tool-output tokens), full-file reads of 1000+ line PRDs (~1.13M),
and full `git diff` inspection (~262k), compounded by long multi-phase sessions that re-send
prior context every turn. The fix is to stop unbounded evidence-gathering and exploit the
fact that project docs follow fixed scaffolds.

## Changes

### 1. New `local-docs/INDEX.md` (agent wayfinder)
Single navigation entry point implementing partial disclosure (task → area → file → section):
- **§A Task → Destination** routing table.
- **§A.2 Skill Directory** — all 13 `skills-engineering` skills as a lookup catalog,
  **invoke only on the user's explicit request, never auto-fire**.
- **§B** directory map (moved out of CLAUDE.md) + conventions; ⚠️ flag on files >1000 lines.
- **§C.0 Scaffold & Template Registry** — per doc type: authoritative scaffold source +
  reusable template file. FR PRD scaffold source = `.specify/templates/prd-template.md`.
- **§C.1–C.5** heading scaffolds for FR PRD, system-prd, schema, tech-spec, sprint reports.
- **§D Code Map** — repomix `--compress` plan (tree + signatures, per-app, periodic regen)
  for indexing `main/` source without reading it whole (Phase 2, pending).

### 2. `CLAUDE.md` / `AGENTS.md` (kept byte-identical mirrors)
- Added **Navigation & Token Governance** section: start at `INDEX.md`; locate before
  reading; read by section not by file; cap search output; soft phase budgets; split phases
  into fresh threads; never re-read generated artifacts in full.
- **Skills** changed from BLOCKING/auto-trigger to **user-triggered** (catalog in INDEX §A.2);
  once the user invokes a skill it is still BLOCKING and `SKILL.md` is authoritative.
- **History restraint** (new governance rule 8): do **not** read update-logs or run
  `git diff`/`git log` per task. Update-logs are read only when history genuinely matters
  **and with user confirmation**, via the `update-logs/README.md` wayfinder to pinpoint one
  entry — never scan the folder; for one FR, prefer that PRD's *Appendix: Change Log*. Git
  defaults to `--stat`/`--name-only`/`--check`. The live doc is the source of truth for
  *what is true now*; history only answers *what changed and why*.
- Removed the verbose `File Structure (local-docs/)` listing (now in INDEX §B); replaced with
  a one-line pointer. Permission table and `main/` read tiers preserved verbatim.

### 3. `local-docs/README.md`
- Added an AI-agent callout pointing to `INDEX.md` as the wayfinder; README remains human
  onboarding. Bumped Last Updated to 2026-06-26.

## Refinement (same day, minor)
Applied four ACI (agent-computer-interface) design principles as governance reinforcements,
and clarified the regime is **for all AI agents/tools, not just Codex** (model- and
harness-agnostic):
- **(a) Search cap:** strengthened to "if a query exceeds ~50 matches, stop and narrow —
  never widen a noisy search."
- **(b) Numbered reads:** prefer `rg -n`/numbered output when range-reading so edits cite
  lines without re-counting (section-reading remains the primary unit, superior to fixed
  line windows for scaffolded docs).
- **(d) Rolling summary:** within a long thread, keep a one-line summary per completed step
  so context degrades gracefully if the thread is not split.
- **(c)** re-aimed from a code linter to a **doc/artifact validator** — deferred to Phase 4.

## Follow-ups (not in this change)
- **Phase 1.5**: PRD template already exists at `.specify/templates/prd-template.md` — INDEX
  points to it; no new file needed.
- **Phase 2**: (i) generate per-app `code-map-*.md` via repomix `--compress`; tune flags and
  cadence; (ii) ship a `search.sh` wrapper around `rg` that **hard-caps** output and prints
  `"N matches — refine query"` past the limit (makes ACI-(a) enforceable, not just advisory).
- **Phase 3**: after 3–5 sessions, compare uncached-input + tool-output per phase vs baseline.
- **Phase 4 (approval-gated)**: FROZEN-skill "quick path" sections; **doc/artifact validator**
  (markdown table integrity incl. literal-`|` rule, relative-link check, PRD-scaffold
  conformance to `.specify/templates/prd-template.md`, Plane-task field checks) — runs after
  edits/generation to reject malformed changes early (ACI-(c)).
