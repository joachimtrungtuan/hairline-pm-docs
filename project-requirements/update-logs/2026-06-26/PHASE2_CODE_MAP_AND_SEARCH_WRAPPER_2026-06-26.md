# Phase 2 — Code Maps + Capped Search Wrapper

**Date**: 2026-06-26
**Type**: Tooling / Navigation infrastructure (token-optimization initiative, Phase 2)
**Scope**: `local-docs/project-automation/scripts/`, `local-docs/project-notes/`, `local-docs/INDEX.md`

This is Phase 2 of the token-optimization initiative. Phase 1 added `local-docs/INDEX.md`
(the agent wayfinder) and the Navigation & Token Governance regime in `CLAUDE.md`/`AGENTS.md`.
Phase 2 makes the §D Code Map real and adds a capped-search entry point.

---

## 1. `search.sh` — capped ripgrep wrapper

**Path**: `local-docs/project-automation/scripts/search.sh` (executable; new `scripts/` dir, not frozen)

A POSIX-friendly bash wrapper around ripgrep that enforces token governance: it counts
matches first and **refuses to dump** results that exceed a hard cap, forcing query
refinement instead of flooding context.

- **Default**: numbered output (`rg -n`), hard cap of **50** matches.
- **Over cap**: prints only `"<N> matches — too many, refine your query (add a path, anchor, or exact term)"` and exits `2` — never dumps the matches.
- **No match**: prints `0 matches`, exits `1`.
- **Within cap**: prints numbered matches (or file list in `-l` mode), exits `0`.
- **Flags**: `-l` files-with-matches mode; `-c N` override the cap; `-h` usage header. Cap also settable via `SEARCH_CAP` env var (the `-c` flag wins).
- **Usage**: `bash local-docs/project-automation/scripts/search.sh [-l] [-c N] PATTERN [PATH ...]`

**Tested on `local-docs/`** (all passed):
- Over-cap: `"the" local-docs/` → `11637 matches — too many…`, exit 2 (refuse path).
- Within-cap numbered: `"Code Map" local-docs/INDEX.md` → 2 numbered lines, exit 0.
- `-l` list mode: small query returns file list, exit 0.
- No match: returns `0 matches`, exit 1.
- `-c` override: raising the cap lets an otherwise-over-cap query emit output.
- `-h`: prints the usage header.

> Implementation note: the match-count pipelines are guarded with `|| true` so that
> ripgrep's non-zero "no matches" exit does not abort the script under `set -euo pipefail`.

---

## 2. Code maps (repomix, structure-only)

Three per-app maps under `local-docs/project-notes/`, each a **directory tree only**
(no file bodies), scoped to source dirs and readable whole. Each file carries a header
recording its scope and an on-demand command for fetching signatures of one subdir.

| File | Source scope | Lines | Bytes |
|---|---|---|---|
| `code-map-backend.md` | `main/hairline-backend` → `app/`, `routes/`, `database/` | 1677 | 69531 |
| `code-map-frontend.md` | `main/hairline-frontend` → `src/` | 1591 | 43882 |
| `code-map-app.md` | `main/hairline-app` → `lib/` | 542 | 17396 |

**Exact working commands**:

```bash
repomix main/hairline-backend/app main/hairline-backend/routes main/hairline-backend/database \
  --no-files --style markdown \
  --ignore "**/vendor/**,**/node_modules/**,**/storage/**" \
  -o local-docs/project-notes/code-map-backend.md

repomix main/hairline-frontend/src --no-files --style markdown \
  --ignore "**/node_modules/**,**/dist/**,**/build/**" \
  -o local-docs/project-notes/code-map-frontend.md

repomix main/hairline-app/lib --no-files --style markdown \
  --ignore "**/.dart_tool/**,**/build/**" \
  -o local-docs/project-notes/code-map-app.md
```

(A `--header-text "..."` describing each map's scope and signature command was also passed.)

**Scoping decision (deviation from the original `--compress` plan):** repomix `--compress`
*does* work (it emits class/function signatures with `⋮` delimiters), but for these apps the
signature dump is far too large to read whole — backend `~50k` lines, frontend `~70k`, app
`~10k` — which would violate the very token governance this initiative enforces. The 2000-line
"readable whole" constraint is the hard requirement, so the maps use `--no-files`
(metadata-only) mode: a navigable directory tree that shows *where* every file lives. When an
agent needs the **signatures** of one area, the map header gives a targeted compress command,
e.g. `repomix main/hairline-backend/app/Models --compress --remove-comments --style markdown -o -`.
Backend `database/` migrations/seeders/factories are kept (tree is cheap) but were the main
reason a whole-backend compress ballooned; the tree handles them fine.

**Verification**: spot-checked the first ~30 tree lines of `code-map-app.md` — confirmed it is
a directory listing (paths only), not file bodies. Maps were not read back in full.

**Cadence**: regenerate weekly or on demand when `main/` source moves materially.

---

## 3. INDEX.md edits

- **§D Code Map**: replaced the "pending — Phase 2" caveat with the three confirmed map
  paths and their line counts; replaced the example `--compress` command with the three
  actually-working `--no-files` commands; added a note explaining why tree-only is used and
  how to get signatures on demand.
- **§B Tools note**: added a short **Tools** subsection pointing to
  `project-automation/scripts/search.sh` as the preferred capped-search entry point (with a
  one-line usage example) and cross-referencing the code maps in §D.

---

## Risks / Notes

- The maps are point-in-time snapshots of `main/` (read-only source); they drift as the dev
  team commits. Workflow in §D handles staleness (expand search there, flag for regeneration).
- The signature-level view is deliberately on-demand, not pre-generated, to respect token
  governance. If a future need arises for a persisted compressed map of a specific small
  module, generate it as a separate scoped file rather than re-compressing a whole app.

---

## Related (minor, same day)

- Created `local-docs/project-automation/plans/token-optimization-phase3-review.md` — the
  Phase 3 review playbook (baseline metrics, per-phase targets, trigger condition, measurement
  method, decision rubric, and an empty results log). Phase 3 is a condition-triggered
  measurement checkpoint (after 3–5 real sessions under the new rules), not build work; the
  playbook makes it resumable from a cold session by reading one file.
- Added `local-docs/project-automation/scripts/regen-code-maps.sh` — re-indexes `main/` into
  the three tree-only code maps on demand (`all` / `backend` / `frontend` / `app`), now with
  `--no-file-summary` + a concise scope header (trims repomix boilerplate; maps re-generated
  at backend 1643 / frontend 1557 / app 508 lines). Added
  `local-docs/project-automation/scripts/README.md` documenting prerequisites, usage, and
  expected output (incl. exit codes) for both `search.sh` and `regen-code-maps.sh`. Updated
  `INDEX.md` §B Tools to reference the regen script and the scripts README.
