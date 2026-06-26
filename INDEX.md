# Hairline Documentation Index (Agent Wayfinder)

**Purpose**: This is the single navigation entry point for AI agents. Before reading
any file, use this index to map **task → area → file → section**, then read **only the
section you need**. Do not scan the tree. Do not read long files whole.

**Last Updated**: 2026-06-26

> Behavior rules (locator-first, phase budgets, no full-file reads) live in
> `CLAUDE.md` / `AGENTS.md` → *Navigation & Token Governance*. This file is **where to
> look**; that file is **how to behave**. Read both once per task, then act.

---

## A. Task → Destination

Find your task, go to the listed area, then jump via the Section Maps in §C.

| If your task involves… | Go to | Then |
|---|---|---|
| A specific feature / requirement | `project-requirements/functional-requirements/frNNN-*/prd.md` | PRD Section Map (§C.1) |
| System-wide requirements, personas, core workflows | `project-requirements/system-prd.md` | §C.2 |
| Database tables, fields, relationships | `project-requirements/system-data-schema.md` | §C.3 |
| Architecture, APIs, integrations, deployment | `project-requirements/system-technical-spec.md` | §C.4 |
| Project principles / scope / vision | `project-requirements/constitution-summary.md` | read top-to-mid only |
| Original client requirements (verbatim) | `project-requirements/transcriptions/` | locate file first |
| Verifying an FR is built correctly | run the `verify-fr` skill | skill is authoritative |
| Breaking a PRD into implementation tasks | run `create-implementation-tasks` skill | — |
| Logging bugs as tasks | run `create-bug-tasks` skill | — |
| Any Plane (issues/cycles/projects) action | run `plane-api-commands` skill | — |
| Checking build/implementation progress | run `check-progress` skill; `progress-tracking/` | — |
| Sprint readiness / client review report | run `sprint-readiness-reporting` skill; `product-plans/` | date folder |
| Status reports / analyses | `reports/YYYY-MM-DD/` | locate by date |
| Test plans / QA | `testing-plans/YYYY-MM-DD/` | — |
| Website / public content | `website-works/` | — |
| Recent doc changes / audit trail | `project-requirements/update-logs/` | read its README first |
| Read / review / analyze main/ source code (only when invited) | see §D Code Map | map first → open only the named files |

Rows above that say "run the X skill" point into the **Skill Directory (§A.2)** — consult
it to pick the right skill, but **invoke only when the user explicitly asks** for that work.

---

## A.2 Skill Directory (invoke only on user request — never auto-fire)

These are the project agent-skills under `project-automation/skills-engineering/`
(FROZEN source-of-truth). This table is a **lookup catalog**: it tells you *which* skill
owns a kind of work so you can load the right `SKILL.md` **when the user triggers it**. Do
not start a skill on your own inference — wait for the user to request that task. Once
invoked, the skill's `SKILL.md` is authoritative; follow it step-by-step.

| Skill | Owns this work — invoke when the user asks to… |
|---|---|
| `verify-fr` | Review/verify FR PRD(s) against constitution, system PRD, transcriptions, dependencies (single or cross-FR). |
| `create-implementation-tasks` | Generate date-stamped Plane-ready implementation tasks from FR gaps / checklist subflows / PRD coverage. |
| `create-bug-tasks` | Draft Plane-ready `[BUG]` task markdown from bug reports, readiness backlogs, or pasted bug lists. |
| `check-progress` | Update one checklist row for a specific MODULE_CODE + FR_CODE pair, verifying FE/BE evidence. |
| `plane-api-commands` | Any Plane API action: refresh metadata, list resources, create/update work items, set parents, add links. |
| `sprint-readiness-reporting` | Start/continue/update sprint readiness reports and fix backlogs from the launch plan or review findings. |
| `verify-design-layout` | Review Figma layouts (PNG/JPG/JSON) against FR screen specs for missing fields, type mismatches, flow gaps. |
| `api-testing` | Test a SINGLE API endpoint with detailed reporting (one endpoint, one scenario). |
| `api-flow-testing` | Run a named multi-step API business flow end-to-end (e.g. inquiry creation, quote acceptance). |
| `api-flow-register` | Research/propose/confirm/register an API flow or endpoint profile (used when a flow is unknown or needs updating). |
| `android-emulator-qa` | Test a SINGLE screen of the Flutter Android app on emulator/device (UI, validation, bug repro, layout). |
| `android-flow-test` | Run a named multi-screen Android app journey end-to-end on emulator/device. |
| `android-flow-register` | Interactively record/update a multi-screen Android testing flow via a live guided session. |
| `gen-code-map` | Generate/refresh the three semantic code maps for `main/` (backend/frontend/app) and check folder drift. |

> **Governance note (pending your decision):** CLAUDE.md currently marks skills as
> **BLOCKING / auto-trigger on frontmatter match**. Your instruction here is the opposite —
> *user-trigger only*. If confirmed, the CLAUDE.md "BLOCKING" wording should change to
> "load and follow the matching skill **when the user invokes that work**, do not auto-fire."

---

## B. File Registry & Conventions

```md
local-docs/
├── README.md                     Human onboarding (people, not routing)
├── INDEX.md                      ← THIS FILE (agent routing)
├── project-requirements/
│   ├── constitution-summary.md   Project principles & scope
│   ├── system-prd.md             System PRD — 33 FRs, personas, workflows  ⚠️ ~2000 lines
│   ├── system-technical-spec.md  Architecture, APIs, deploy               ⚠️ ~2070 lines
│   ├── system-data-schema.md     97 tables, relationships                 ⚠️ ~2027 lines
│   ├── functional-requirements/  frNNN-slug/prd.md  (36 FRs; many ⚠️ >1000 lines)
│   ├── transcriptions/           Client requirements, verbatim
│   └── update-logs/              Change history (has its own README index)
├── project-automation/
│   ├── skills-engineering/       FROZEN — source-of-truth SKILL.md defs
│   ├── commands/                 FROZEN — Cursor rule adaptations
│   ├── workflows/                FROZEN — Antigravity workflow adaptations
│   ├── task-prompt/              FROZEN — prompt/issue templates
│   ├── task-creation/YYYY-MM-DD/ Generated task breakdowns & verify reports
│   │   └── plane-api/            Plane credentials (.env) & system vars
│   ├── plans/                    Automation plans
│   └── notes/                    Automation notes
├── product-plans/YYYY-MM-DD/     Roadmaps, sprint review/readiness; template/
├── progress-tracking/            Ongoing status trackers
├── project-notes/                Ad-hoc notes, decisions, dev-related-issues/
├── reports/YYYY-MM-DD/           Status reports & analyses
├── testing-plans/YYYY-MM-DD/     Test plans; testing-credentials/
└── website-works/                website-requirements/, project-static-content/
```

**Conventions**

- Dated artifacts live in `YYYY-MM-DD/` folders — locate by date before reading.
- FR folders are `frNNN-kebab-slug` (e.g. `fr022-search-filtering`); the doc is always `prd.md`.
- Module codes: Patient `P-01..P-07`, Provider `PR-01..PR-07`, Admin `A-01..A-10`, Shared `S-01..S-06`.
- ⚠️ = file exceeds ~1000 lines → **never read whole; range-read via §C**.

**Tools**

- **Capped search:** prefer `project-automation/scripts/search.sh` over raw `rg` — it
  numbers output and refuses to dump more than 50 matches (prints a count + "refine your
  query" and exits non-zero), enforcing the locate-then-narrow rule.
  Usage: `bash local-docs/project-automation/scripts/search.sh "PATTERN" <path>`
  (`-l` files-only, `-c N` to override the cap, `-h` for help).
- **Code maps:** see §D — `project-notes/code-map-{backend,frontend,app}.md` (curated semantic
  maps). Maintained by the **`gen-code-map`** skill (drift check + curated refresh); not a script.
- **Script docs:** `project-automation/scripts/README.md` — prerequisites, usage, and expected
  output (incl. exit codes) for `search.sh`.

---

## C. Section Maps & Templates (read headings, jump to one section)

Most Hairline docs follow a **fixed heading scaffold**. To navigate any of them:

```bash
rg -n "^## " <file>     # list section anchors (cheap)
sed -n 'START,ENDp' <file>   # read only the chosen section
```

Anchor *text* is stable; line numbers below are hints that drift — confirm with the `rg` above.

### C.0 — Scaffold & Template Registry

For each doc type: where its structure is **defined** (template/source) and the section map to use.

| Doc type | Authoritative scaffold source | Reusable template file | Section map |
|---|---|---|---|
| FR PRD (`frNNN/prd.md`) | **`.specify/templates/prd-template.md`** (canonical); `verify-fr/SKILL.md` section contract | `.specify/templates/prd-template.md` | §C.1 |
| System PRD | `system-prd.md` itself | — | §C.2 |
| Data schema | `system-data-schema.md` itself | — | §C.3 |
| Technical spec | `system-technical-spec.md` itself | — | §C.4 |
| Sprint client review report | `sprint-readiness-reporting/SKILL.md` | `product-plans/template/client-sprint-review-report-template.md` | §C.5 |
| Sprint readiness / fix backlog | `sprint-readiness-reporting/SKILL.md` (+ `references/reporting-rules.md`) | `product-plans/template/sprint-readiness-fix-backlog-template.md` | §C.5 |
| Implementation task doc | `create-implementation-tasks/references/task-format.md` | (format spec, not a fill-in) | run skill |
| Bug task doc | `create-bug-tasks/references/` | — | run skill |
| Android QA test report / flow script | `android-emulator-qa/SKILL.md` | `android-emulator-qa/assets/test-report-template.md`, `assets/flow-script-template.md` | run skill |
| Design-layout review report | `verify-design-layout/SKILL.md` | `verify-design-layout/assets/report-template.md` | run skill |
| Update-log entry | CLAUDE.md → Update Log Protocol | dated exemplars in `update-logs/` | — |

> **Speckit templates** live in `.specify/templates/` (project root, read-only reference):
> `prd-template.md` (canonical FR PRD scaffold — matches §C.1), plus `plan-template.md`,
> `tasks-template.md`, `checklist-template.md`, `agent-file-template.md`. Use
> `fr022-search-filtering/prd.md` as a complete filled exemplar.

### C.1 — FR PRD scaffold (identical across all 36 FRs)

```md
## Executive Summary
## Module Scope            (Multi-Tenant Architecture / Breakdown, Entry Points)
## Business Workflows      (Main Flows, Alternative Flows)
## Screen Specifications   ← usually the LARGEST block; range-read one platform only
      ### 1. Patient Platform Screens
      ### 2. Provider Platform Screens
      ### 3. Admin Platform Screens
## Business Rules
## Success Criteria
## Dependencies            (Internal / External / Data)
## Assumptions
## Implementation Notes
## User Scenarios & Testing
## Functional Requirements Summary
## Key Entities
## Appendix: Change Log
## Appendix: Approvals
```

Matches `.specify/templates/prd-template.md` (canonical). Confirm live anchors with
`rg -n "^## " <prd.md>` — a few early FRs may omit the trailing appendices.

### C.2 — system-prd.md

```md
## Executive Summary · ## Product Overview · ## User Personas · ## Core Workflows
## Functional Requirements   ← largest; FR-001..FR-033 in order, grep "FR-0NN"
## Non-Functional Requirements · ## Edge Cases & Exception Handling
## Success Criteria · ## Out of Scope · ## Assumptions & Dependencies · ## Appendix
```

### C.3 — system-data-schema.md

```md
## Executive Summary · ## Entity Relationship Overview
## Core Entities          ← largest (~line 79–1200); grep the table name you need
## Supporting Entities · ## Permission & Role Management (Spatie)
## OAuth & Authentication (Laravel Passport)
## Database Constraints & Relationships Summary · ## Data Types & Conventions
## Data Security & Privacy · ## Migration Strategy · ## Database Seeding
## Performance Optimization · ## Appendix
```

### C.4 — system-technical-spec.md

```md
## Executive Summary · ## System Architecture · ## Core Workflow Implementation
## Backend Architecture   ← largest (~line 213–945)
## Frontend Architecture (Web) · ## Mobile Architecture · ## Third-Party Integrations
## Security Implementation · ## Performance Optimization · ## Testing Strategy
## Deployment · ## Monitoring & Logging · ## Appendix
```

### C.5 — Sprint report scaffolds (`product-plans/`)

Driven by the `sprint-readiness-reporting` skill; copy the template, fill per skill rules.

```md
client-sprint-review-report-template.md
  # Sprint [N] Client Review Report
  ## Document Control
  # 1. Executive Summary
  # 2. Launch Plan Position Snapshot  (2.1 Launch Progress Track · 2.2 Launch Readiness Gauge)
  # 3. Sprint Outcomes
  # 4. Open Items, Risks & Next Sprint Direction

sprint-readiness-fix-backlog-template.md
  # Sprint [N] Readiness & Fix Backlog
  ## Document Control & Sprint Summary · ## How To Use This Template
  # 1. Sprint Scope From Launch Plan  (1.1 Modules · 1.2 User Stories · 1.3 Deferred/Out of Scope)
  # 2. Sprint Fix Backlog  (2.1 Sprint-Level Blockers · 2.2 Module Fix Backlog per [Module ID])
  # 3. Not For This Sprint
```

Other skill-owned templates (open only when running that skill):
`android-emulator-qa/assets/{test-report-template,flow-script-template}.md`,
`verify-design-layout/assets/report-template.md`,
`create-implementation-tasks/references/task-format.md`.

---

## D. Code Map (main/ source)

`main/` is the dev team's source (never edit; read only when invited per CLAUDE.md).
It changes constantly, so consult the **semantic code maps** before opening files.

> **Locator, not evidence:** the maps tell you WHERE to look; open the named source to confirm
> any finding. Their job is to replace broad searches — never to substitute for reading the code.

- Code maps (curated **folder-group** maps — purpose + module/FR bindings + entry points
  per folder group, NOT a raw file tree; small, readable whole):
  | Map | Codebase | Tenants | ~Lines |
  |---|---|---|---|
  | `project-notes/code-map-backend.md` | `main/hairline-backend` (Laravel API) | all 3 | ~204 |
  | `project-notes/code-map-frontend.md` | `main/hairline-frontend` (web) | Provider + Admin | ~116 |
  | `project-notes/code-map-app.md` | `main/hairline-app` (Flutter) | Patient | ~105 |
- **Workflow:** read the relevant map → it names the folder group, its modules/FRs, and the
  entry-point files → open only those. If you need the **signatures** of one subdir, run the
  on-demand command in the map's header (do not persist it):
  `repomix <subdir> --compress --remove-comments --style markdown -o -`.
- **Refresh / drift:** the maps are maintained by the **`gen-code-map` skill** (user-triggered).
  Its bundled `scripts/check-code-map-drift.sh` flags added/removed folders vs the last snapshot
  (`project-notes/.code-map-snapshots/`); the skill then refreshes only the changed groups and
  re-accepts the snapshot. Run the skill when `main/` has been restructured or a map looks stale.
- **Expand only when the map proves wrong** — then fix it (or invoke `gen-code-map`).
