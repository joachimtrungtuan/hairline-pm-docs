---
name: gen-code-map
description: Generate or refresh the persistent semantic code maps for the three Hairline codebases (backend / web frontend / Flutter app). Use when asked to generate, regenerate, or refresh the code map(s), to check code-map drift, or after the dev team restructures folders in main/. User-triggered only — do not run automatically.
---

# Generate Code Map (gen-code-map)

## Purpose

Maintain the **persistent, curated code maps** that bind the dev team's source code
(`main/`, read-only) to the project's own module codes and FRs. The maps are
**folder-group level, not file level** — they describe what each folder group is for and
which modules/FRs it serves, so they stay useful and age slowly (folders change rarely;
individual files churn every commit). They are the wayfinder into code, replacing raw
directory trees.

## Persistent code map paths (3 codebases ↔ tenants)

These three files are the authoritative outputs. Always read/refresh these exact paths —
do not create new map files or write maps elsewhere.

| Map file (persistent) | Codebase | Stack | Tenant(s) it serves |
|---|---|---|---|
| `local-docs/project-notes/code-map-backend.md` | `main/hairline-backend` | Laravel API | **All 3** — Patient, Provider, Admin (one REST API) |
| `local-docs/project-notes/code-map-frontend.md` | `main/hairline-frontend` | Web (React/TS) | **Provider + Admin** ("hairlineProvider" + "hairlineTeam") |
| `local-docs/project-notes/code-map-app.md` | `main/hairline-app` | Flutter / Dart | **Patient** mobile only (iOS/Android) |

Folder snapshots used for drift detection live in
`local-docs/project-notes/.code-map-snapshots/` (one `.dirs` file per codebase).

## Hard Rules

- `main/` is **READ-ONLY** — never edit it. Read it efficiently: prefer directory listings,
  `routes/api.php` prefixes, and the tech-spec architecture sections over reading whole
  implementation files. Open a source file only to resolve one specific question, and only its top.
- Write **only** to the three `code-map-*.md` files above (and snapshots via the script).
- **Folder-group altitude.** Document folder groups, not individual files. Breadth over depth.
- **Accuracy over coverage.** If a folder's module/FR binding is unclear, write `—` and note it
  in a "Notes / unmapped" section. Never guess a binding.
- **Never read a finished map back in full** to consume it elsewhere, and **never persist
  signature dumps** — signatures are fetched on demand (see the command in each map's header).
- Do not write one-off scripts. Use the bundled `scripts/check-code-map-drift.sh` for detection.
- Keep each map small (target < ~400 lines; hard ceiling ~2000).

## Files

- `scripts/check-code-map-drift.sh` — deterministic drift detector (folder diff vs snapshot; no LLM, no file reads). Modes: default = check, `accept` = save snapshot. See `-h`.
- `references/generation-rules.md` — the map output format, the module/FR binding rules, inputs to use, and altitude guidance. Load this before generating or refreshing.

## Workflow

1. **Detect drift.** Run `bash scripts/check-code-map-drift.sh` (or `... <backend|frontend|app>`
   for one). It prints added/removed folders per codebase, or "no drift".
   - If the user asked for a **full regeneration** of a map, skip to step 3 for that codebase.
2. **No drift + no explicit regen request →** report "maps current" and stop. Do not refresh.
3. **Refresh the affected codebase(s).** Load `references/generation-rules.md`. For each codebase
   needing work, update **only the folder-groups affected by the drift** (added → add a group;
   removed → drop/merge its group; renamed/restructured → revise). For a full regen, rewrite the
   whole map per the rules. Bind every group to modules (P-/PR-/A-/S-) and FRs using
   `routes/api.php`, the FR→module table in `system-prd.md`, and the tech-spec architecture sections.
4. **Verify** a sample: pick 2–3 refreshed groups and confirm the folder exists and the
   module/FR binding is defensible (e.g. against the route prefix).
5. **Accept the snapshot.** Run `bash scripts/check-code-map-drift.sh accept` (or per codebase)
   so the next drift check compares against the new structure.
6. **Log** per the Update Log Protocol (this is a doc change to the maps).

## Notes

- The maps are point-in-time; they drift as the dev team commits. This skill's whole job is to
  make that drift visible (step 1) and cheap to reconcile (step 3 touches only changed groups).
- Known reality (keep accurate): the web frontend is Provider+Admin (not patients); the Flutter
  app is Patient-only; the tech-spec's "React Native" mobile note is stale (actual stack is Flutter).
