# Code Map Generation Rules

Reference for the `gen-code-map` skill. Defines the map format, binding rules, inputs, and
altitude. Load this before generating or refreshing any `code-map-*.md`.

## Output format (per map file)

Each map starts with a one-line H1 title, a fixed header block, and a short intro paragraph,
then one `##` section per folder-group.

```md
# Code Map — <codebase> (<stack>; <which tenants/platforms it serves>)

Curated folder-group map (folder-level, not file-level — refresh when modules are
added/restructured, flagged by check-code-map-drift.sh). For the SIGNATURES of one
subdir on demand (do NOT persist): repomix <subdir> --compress --remove-comments --style markdown -o -
**Locator, not evidence:** use this map to pinpoint WHERE to look, then read the actual
source for any finding — it exists to prevent broad searches, never to replace reading code.

<intro: stack, architecture pattern, how module boundaries are expressed (e.g. URL
prefixes in routes/api.php, or features/<x> folders), and the module-code legend.>

## <folder or folder-group path>
- **Purpose:** one line — what lives here and why it matters.
- **Modules:** P-0x / PR-0x / A-0x / S-0x codes (or `—` if cross-cutting/infra).
- **FRs:** FR-0xx references (or `—` if infrastructural).
- **Entry points / key files:** the 1–3 files to open first.

## <next group> …

## Notes / unmapped
<folders deliberately left `—`: framework/infra, dev artifacts, genuinely ambiguous areas —
with a one-line reason each.>
```

## Altitude (how to group)

- Group at a sensible domain level: e.g. backend `app/Http/Controllers/Patients/` is one group;
  `app/Models/` is one; `routes/` is one. Frontend: group by `features/<area>`, `pages/<area>`,
  `components/<area>`. Flutter: group by `lib/src/features/<feature>` and the core/di/services dirs.
- Breadth over depth: cover **every significant folder** as a group; never enumerate files.
- Target each map < ~400 lines (hard ceiling ~2000).

## Module / FR binding inputs (cheap first)

1. The **current** `code-map-*.md` (when refreshing) — start from what's there; change only what drifted.
2. `routes/api.php` (backend) — the URL-prefix tree (`/patient*`, `/provider*`, `/admin*`, shared
   `/inquiry` `/quote` `/chat` …) is the authoritative map of which controller serves which platform.
3. The **FR → module table** in `local-docs/project-requirements/system-prd.md` (`## Functional
   Requirements`) and the module list in `local-docs/README.md` (read the README list first — cheap).
4. Architecture prose in `local-docs/project-requirements/system-technical-spec.md` — read only the
   `Backend Architecture` / `Frontend Architecture (Web)` / `Mobile Architecture` sections
   (find ranges with `rg -n "^## "`).
5. Targeted entry-file reads only to resolve a specific binding question (open the top, not the whole file).

Models: cross-reference `system-data-schema.md` entities conceptually — note "maps to schema
entities"; do **not** read the whole schema.

## Module-code legend

Patient `P-01..P-08` · Provider `PR-01..PR-07` · Admin `A-01..A-10` · Shared `S-01..S-06`.
FRs run `FR-001..FR-035`.

## Discipline

- Accuracy over coverage: unclear binding → `—` + a Notes line. Never guess.
- Read-only `main/`; efficient reads (listings, routes, tech-spec) over whole files.
- Keep the on-demand signature command in the header; never persist signature dumps.
- Known reality to preserve: web frontend = Provider+Admin; Flutter app = Patient-only; the
  tech-spec "React Native" mobile note is stale (actual stack = Flutter).
