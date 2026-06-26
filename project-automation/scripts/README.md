# Project Automation Scripts

General-purpose utilities supporting the token-optimization initiative. Plain Bash; run
from anywhere (they locate the repo root from their own path).

| Script | What it does | When to run |
|---|---|---|
| `search.sh` | Capped ripgrep — refuses to dump huge result sets | Every time you search docs/code |

> **Code maps** are no longer maintained by a script here. Generating/refreshing the three
> semantic code maps (`local-docs/project-notes/code-map-{backend,frontend,app}.md`) and
> detecting folder drift is now the **`gen-code-map` skill**
> (`local-docs/project-automation/skills-engineering/gen-code-map/`). Its bundled
> `scripts/check-code-map-drift.sh` does the deterministic drift detection; the skill workflow
> handles the curated refresh. Invoke the skill when asked to refresh code maps.

---

## Prerequisites

- **bash** (project shell is zsh, but scripts use `#!/usr/bin/env bash`).
- **ripgrep** (`rg`) — required by `search.sh`. Check: `rg --version`. Install: `brew install ripgrep`.

(`repomix` is only needed for the optional **on-demand** signature command printed in each code
map's header — not by any script here.)

---

## `search.sh` — capped search

Use this instead of a bare `rg` so a broad query can't flood context. It counts matches first;
if the count exceeds the cap it prints **only** the count + a hint and exits — it never dumps
the matches.

### Usage
```bash
bash local-docs/project-automation/scripts/search.sh [-l] [-c N] PATTERN [PATH ...]
```
- `-l` — files-with-matches mode (list matching files only).
- `-c N` — override the cap for this run (default **50**; also settable via `SEARCH_CAP` env).
- `-h` — help.
- `PATTERN` — ripgrep pattern (required). `PATH ...` — optional; defaults to current dir.

### Examples
```bash
# Find FR references in one file (numbered output)
bash local-docs/project-automation/scripts/search.sh "FR-0[0-9][0-9]" local-docs/project-requirements/system-prd.md

# Just list files that mention a term
bash local-docs/project-automation/scripts/search.sh -l "transcription" local-docs/

# Allow up to 100 matches this time
bash local-docs/project-automation/scripts/search.sh -c 100 "TODO" local-docs/
```

### What to expect (exit codes)
| Situation | Output | Exit |
|---|---|---|
| Matches ≤ cap | Numbered `rg -n` results (or file list with `-l`) | `0` |
| Matches > cap | `"<N> matches — too many, refine your query (add a path, anchor, or exact term)"` — no matches printed | `2` |
| No matches | `0 matches` | `1` |
| Bad args | error message + usage | `64` |

> Exit `1`/`2` are **expected signals**, not script failures. `2` means "narrow the query"
> (add a path, an anchor like `^`, or a more exact term) — don't widen it.

---

## Related

- Capped-search and code-map work are part of the token-optimization initiative — see
  `INDEX.md` §B (Tools) and §D (Code Map), the `gen-code-map` skill, and the Phase 3 review
  playbook at `project-automation/plans/token-optimization-phase3-review.md`.
