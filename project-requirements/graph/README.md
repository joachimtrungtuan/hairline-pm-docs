# Requirements graph

This folder holds the requirements graph. It stores FRs, stages, actors, entities, fields, rules, events, settings, screens and sources as nodes, and the typed edges between them. `graph.db` (SQLite) is the only place graph data lives. `schema.yaml` defines the node types, the attributes each type allows, the ID pattern for each type, the edge verbs with the node-type pairs they may join, and the closed value lists.

## Contents

- `schema.yaml`: the graph schema. Changing node types, verbs or enum values counts as a schema migration, so back up `graph.db` first.
- `graph.db`: the graph database. It has six tables: `nodes`, `fields`, `enum_values`, `edges`, `sources` and `changes`.
- `scripts/common.py`: loads and validates `schema.yaml`, and opens the DB with foreign keys enforced.
- `scripts/init_db.py`: creates an empty `graph.db`.
- `scripts/test_init_db.py`: tests for the schema loader and the database rules.
- `scripts/migrate_schema_v5.py`: moves a version 4 `graph.db` to schema version 5 (see "Schema version 5" below).
- `scripts/migrate_schema_v6.py`: moves a version 5 `graph.db` to schema version 6 (see "Schema version 6" below).
- `scripts/migrate_schema_v7.py`: moves a version 6 `graph.db` to schema version 7 (see "Schema version 7" below).
- `scripts/migrate_schema_v8.py`: moves a version 7 `graph.db` to schema version 8 (see "Schema version 8" below).
- `scripts/check_crs.py`: checks that every Approved Change Request ID appears in its PRD's Appendix: Change Log (exit 1 when one does not; Proposed CRs are listed, not checked, and stay out of the graph, D42).
- `scripts/headless_review.sh`: runs one checklist review through a headless OpenCode model (see "Headless review wrapper" below).
- `backups/`: dated copies of `graph.db`, written before it is replaced.
- `checklists/`: the review and migration checklists every repeated task runs from (`checklists/README.md` lists them, their versions and how a brief must cite them).

## Database rules

The database enforces these rules itself, so a script with a bug cannot break them:

- Every reference column is a foreign key. A node cannot be deleted while something still references it.
- Triggers check that each reference points at the right node type:
  - `nodes.owner_fr` must point at an FR.
  - `fields.id` must be a Field node.
  - `fields.entity_id` must point at an Entity.
  - `fields.calculated_by` must point at a Rule.
  - `sources.id` must be a Source node.
  - `changes.source_id` must point at a Source.
- Nodes are never deleted. Retire a node by setting its `status`. A node's `id` and `type` never change; to rename a node, change its `title`.
- A `fields` row's `id`, `entity_id` and `name`, and a `sources` row's `id`, never change, so a detail row stays attached to its node.
- `changes` is append-only: its rows cannot be updated or deleted.
- When a field is deleted, its `enum_values` rows are deleted with it.
- The database rejects duplicate edges `(from_id, verb, to_id)`, duplicate field names on the same entity, and duplicate enum values on the same field.

- Dashboard totals that no PRD Key Entity owns live on an Entity marked as an aggregate view (not stored), one Field per total with `calculated_by` set. Approved 2026-11-09; see `checklists/migrate-fr.md`.

## Setup

Run these from this folder with the Apple system interpreter, `/usr/bin/python3`. The scripts need only the standard library plus PyYAML, which that interpreter already ships (6.0.3 on macOS 26). Since 2026-11-09 this is the documented route: the workspace's command hook blocks any command that names a `.venv` path, so the earlier local virtual environment is no longer used. If a machine's system python lacks PyYAML, create a venv elsewhere (outside this tree) and substitute its interpreter in the commands below.

## Create the database

```bash
/usr/bin/python3 scripts/init_db.py                # creates graph.db here
/usr/bin/python3 scripts/init_db.py path/to/x.db   # or at another path
/usr/bin/python3 scripts/init_db.py --force        # replaces graph.db after copying it to backups/graph-YYYYMMDD-HHMMSS.db
```

Without `--force`, the script will not overwrite an existing database. `--force` replaces the database with an empty one, so all graph data is lost unless you restore the backup.

## Write and query

`scripts/write.py` is the only way to change the graph. It applies one change-set file (JSON for `.json`, YAML otherwise) in a single transaction. A change-set has `reason`, `by`, an optional `source_id` (a Source node), and a list of `operations`: `add_node`, `update_node`, `retire_node`, `add_field`, `update_field`, `add_enum_value`, `retire_enum_value`, `add_edge`, `remove_edge`, `add_source` and `merge_node`. The keys of each operation are listed at the top of the script. When `add_enum_value` has no `sort_order`, the value goes after the field's current values (highest `sort_order` plus one, or 0 for the first). Every operation is checked against `schema.yaml` first; if any check fails, nothing is written and each problem is printed with its operation index, such as `operations[3] (add_edge): ...`. Each applied change-set adds one `changes` row per attribute changed, all under one generated `changeset_id`, and raises `version` by one on every existing node it touched. Exit codes: 0 applied, 1 change-set invalid, 2 database error.

```yaml
# changes/add-quote-expiry.yaml
reason: Quote expiry agreed in meeting 2
by: joachim
source_id: SRC-MTG-002-D03
operations:
  - {op: add_node, id: SET-quote-expiry-window, type: Setting, owner_fr: FR-004, title: Quote expiry window, attrs: {default: "14", unit: days}}
  - {op: add_edge, from: REQ-004-012, verb: governed by, to: SET-quote-expiry-window}
```

```bash
/usr/bin/python3 scripts/write.py changes/add-quote-expiry.yaml
```

`merge_node` (keys `survivor`, `loser`) folds a duplicate Rule into the one that stays. A Rule has one text, so repeats become edges, not nodes. Both nodes must be active, of one type, and of a type whose schema allows the `aliases` attribute (today only Rule). Every edge of the loser, in either direction, moves to the survivor; an edge the survivor already has is dropped rather than duplicated, and a `calculated by` edge moves together with its `fields.calculated_by` column. The loser's id, then the loser's own aliases, are appended to the survivor's `aliases` (comma-separated, no repeats), so old PRD citations of the loser still resolve. The loser is then retired. The merge is part of its change-set's single transaction, and each step is a `changes` row.

```yaml
reason: REQ-004-031 repeats REQ-004-012 under a second screen
by: joachim
operations:
  - {op: merge_node, survivor: REQ-004-012, loser: REQ-004-031}
```

`scripts/query.py` only reads. It prints a plain table, or JSON with `--json`, and takes `--db PATH`. Subcommands: `impact <node-id> [--depth N]` (everything within N hops through any edge, default 2), `lifecycle <timeline>`, `cites <node-id>`, `fr <FR-id>`, `history <node-id>`, `at <node-id> <ISO-timestamp>` (attributes at that time; a timestamp without an offset is read as UTC), `changeset <changeset-id>` and `duplicates [--text "<statement>"]`.

`duplicates --text "<statement>"` lists the active Rules whose statement equals (`exact`, score 1.0) or is near (`similar`, with its score) the candidate statement. Run it before adding any Rule; no rows means no duplicate. Without `--text` it lists every duplicate pair of active Rules, with both owners and statements. It uses the same matching as lint L12.

```bash
/usr/bin/python3 scripts/query.py impact SCR-004-01 --depth 2
```

Tests: `/usr/bin/python3 scripts/test_write_query.py`.

## Lint, export and render

These three scripts only read the database. Each takes `--db PATH` to use a DB other than `graph.db`.

`scripts/lint.py` checks every active node against the guardrails (rules L01 to L19, listed at the top of the script). It prints one row per finding, or `--json`, and exits 1 if there is any finding, 0 if the graph is clean, 2 on an error. Each finding ID is the rule code plus its subject, such as `L03:SCR-004-01`, so counts can be compared between runs. `--fr FR-004` limits the check to nodes that FR owns.

```bash
/usr/bin/python3 scripts/lint.py --fr FR-004
```

L12 flags duplicate Rule statements, one finding per Rule listing its partners. Statements are first normalised: lowercased, punctuation replaced by a space, whitespace collapsed, and the words system, must, shall, the, a and an removed. Equal normalised statements are reported as `same text`. Others are reported as `similar` when difflib's character ratio of the two normalised statements is at least 0.8 (pairs whose word-level ratio is below 0.5 are skipped first, for speed). At 0.8 the 1079 REQ lines of the frozen PRDs give 34 pairs, 4 of them exact. A similar pair can be two different rules worded alike, so a person decides: merge it with `merge_node`, or keep both. L13 flags a Rule with no `applies at` edge at all. L02 also covers that case, and additionally fires when every `applies at` edge ends at a retired Stage.

`scripts/export.py` writes `graph.json` for the viewer: active nodes, fields, enum values, edges and sources, each list sorted so the file diffs cleanly. `--include-retired` adds retired nodes. History is summarised in a top-level `changes` array, one entry per change-set newest first (`id`, `at`, `changed_by`, `reason`, `source_id`, the sorted `nodes_added` and `nodes_updated` ids, `edges_added`, `edges_removed` and `rows`), which the viewer's Changes tab lists; individual change rows stay in `graph.db`.

```bash
/usr/bin/python3 scripts/export.py                 # writes graph.json here
```

`scripts/render.py` renders the graph-owned sections of one FR PRD as markdown: Scope, Actors, Workflows, Screen Specifications, Business Rules, Data, Events, Settings, Dependencies, Sources and Change Log. Rules owned by another FR appear only as a `[REQ-NNN-NNN] title` citation. The output is derived, so hand edits are lost on the next render.

```bash
/usr/bin/python3 scripts/render.py FR-004 --out /tmp/fr-004.md   # stdout without --out
```

Tests: `/usr/bin/python3 scripts/test_lint_export_render.py`.

## Headless review wrapper

`scripts/headless_review.sh` runs one checklist-driven review of a frozen FR PRD through a headless OpenCode model with restricted permissions (no shell, no network, writes only `report.md` and `status.json` in the output folder). The controller pre-computes the graph query, so the model never executes anything; the PRD, the checklist and the query result are symlinked into `<output-dir>/in`. Exit code 0 means the report was written, 124 a timeout, anything else an OpenCode failure; `status.json` is always written. It runs the scripts with `/usr/bin/python3`.

```bash
scripts/headless_review.sh <model> <FR-id> <checklist-path> <output-dir> [timeout-seconds]
scripts/headless_review.sh opencode-go/deepseek-v4.1-flash FR-025 local-docs/project-requirements/graph/checklists/completeness-check.md /tmp/oc-fr025 900
```

The first paired runs (2026-11-09, `plans/reports/tester-261109-headless-trial.md`) found DeepSeek the only working model, with 87 % agreement against a Sonnet run on FR-025; FR-008 timed out at 900 s and was re-run with Sonnet.

## Change-set files and replay

Files under `changesets/` are kept so a change-set can be reviewed before and after it is applied. They are a record, not a rebuild script: each one was validated against the schema version in force when it was written, so a later schema change (for example a new required attribute) can make an older file fail on a fresh database. Recovery is from `backups/`, and history is the `changes` table in `graph.db`. Do not edit an applied change-set file to make it replay.

## Schema version 5

Version 5 added the edge verb `references` (pairs `[FR, Rule]`: an FR that repeats a Rule owned by another FR cites it instead of copying it) and the optional Rule attribute `aliases`. `init_db.py` writes the verb list into a CHECK on `edges.verb`, so the edges table had to be rebuilt; the script below did that. It is kept for older copies of the DB:

```bash
/usr/bin/python3 scripts/migrate_schema_v5.py      # backs up graph.db to backups/ first; --db PATH for another file
```

## Schema version 6

Version 6 (D42, applied 2026-11-10) adds the flow model:

- Node type `Step` (`STP-NNN-NNN`, owned by the FR whose PRD describes it): one action in a flow. Optional attrs `description`, `prd_ref`, and `handoff_to` / `handoff_from`, which name a step in another FR until a cross-FR `next` link replaces them.
- Node type `Flow` (`FLW-...`, no owner): a named start point, attr `kind` (`main`, `alternative` or `journey`). Its path is the `next` links from the Step it `starts at`, so a journey can cross FRs.
- Verbs `done by` (Step to Actor), `at` (Step to Stage), `on` (Step to Screen), `applies` (Step to Rule), `next` (Step to Step; optional attrs `condition` = the Rule id that picks the branch, `label`, `back`) and `starts at` (Flow to Step).
- An Event may now be emitted at several Stages; L04 fires only when it has none.

New lint rules: L14 a Step no Flow reaches (Steps with `handoff_from` are skipped); L15 a `next` link back to an earlier Stage of the same timeline without `back: true`; L16 a Step's Actor with no `acts in` edge to its Stage; L17 a Step without a `done by` Actor or without exactly one `at` Stage; L18 an open hand-off; L19 a `next` condition that is not an active Rule.

Node types and verbs are CHECK constraints in the DDL, so the migration builds a fresh DB from the version 6 DDL, copies every table row by row with its rowid, checks the copy (row equality, foreign keys, integrity), and swaps it in after a backup:

```bash
/usr/bin/python3 scripts/migrate_schema_v6.py      # backs up graph.db to backups/ first; --db PATH for another file
```

Product Owner decisions from the MTG-002 decision log are Source nodes `SRC-PO-001-<code>` (kind `decision item`, parent `SRC-PO-001`, kind `decision log`), so Rules can cite them with `decided by`.

## Schema version 7

Version 7 (D44, applied 2026-11-10) adds the value `system` to the `actor_group` enum: the Hairline platform itself, acting for the steps it performs automatically. One Actor, `ACT-system`, carries that group, so a Step the PRD attributes to "System" can be `done by` it. Groups are now `admin`, `provider`, `patient` and `system`. External services (payment gateway, email and SMS providers) are not the system; version 8 gives them their own group.

`actor_group` lives only in the JSON attrs of Actor nodes, not in a CHECK or trigger, so no table changes. The migration checks that the DB's DDL equals what `init_db.py` writes for the version 7 schema, backs up `graph.db`, and sets `PRAGMA user_version` to 7:

```bash
/usr/bin/python3 scripts/migrate_schema_v7.py      # backs up graph.db to backups/ first; --db PATH for another file
```

## Schema version 8

Version 8 (D45, applied 2026-11-10) adds the value `external` to the `actor_group` enum: a service outside Hairline that performs a step itself. External services are not the system, so each gets its own Actor: `ACT-stripe` (Stripe), `ACT-email-provider` (the email provider) and `ACT-rate-source` (the exchange-rate source). A Step whose subject is the service, such as "Stripe webhook is received", is `done by` that Actor. Hairline's own modules stay in the system: the Payment Service (S-02) is part of the platform, so its Steps are `done by` `ACT-system` (D46). Groups are now `admin`, `provider`, `patient`, `system` and `external`.

As in version 7, only `PRAGMA user_version` changes. The migration checks that the DB's DDL equals what `init_db.py` writes for the version 8 schema, backs up `graph.db`, and sets `PRAGMA user_version` to 8:

```bash
/usr/bin/python3 scripts/migrate_schema_v8.py      # backs up graph.db to backups/ first; --db PATH for another file
```

## Run the tests

From this folder:

```bash
/usr/bin/python3 -m unittest discover -s scripts -p "test_*.py" -q
```

The tests use temporary databases. They never touch `graph.db`.

## Viewer

`viewer/index.html` is a read-only review page for `graph.json`. Use it to check what a migration batch added. It has three parts. **Timelines** shows one lane per timeline, the `follows` order, the `enters from` and `joins` links between lanes, and the actors in each stage. **By FR** lists each FR's owned rules, entities with their fields and enum values, events, settings and screens. The **node panel** shows a node's attributes and its in-edges and out-edges. A search box finds nodes by id or title. The page works offline and needs no build step.

Run `scripts/export.py` first so `graph.json` is current. Then, from this folder:

```bash
python3 -m http.server 8765
```

and open http://localhost:8765/viewer/ . You can also open `viewer/index.html` straight from disk. The browser will block the automatic load, so drop `graph.json` onto the page or pick it with the file picker. The URL hash holds the selected node id (for example `#STG-main-06-treatment`), so browser back and forward move between the nodes you have opened.

### 3D viewer

`viewer/3d.html` shows every node and edge of `graph.json` as an orbitable 3D graph. Open it from `viewer/index.html` ("3D view") or directly. From disk the browser blocks the automatic load of `../graph.json`, so drop the file onto the page or pick it, as in the 2D viewer; with `python3 -m http.server 8765` it loads by itself. Nothing is fetched from the network.

- **Look:** colour by node type (the legend lists the colours and has a toggle and a shown/total count per type), FR and Stage nodes largest. Hover a node or an edge for its label. Derived edges (FR active in Stage, computed by `export.py`) are dashed orange; the "Derived" box and the "Edge verbs" list switch edges on and off.
- **Click a node** to open the side panel: attributes, field detail and enum values, the Source records behind it, and every in-edge and out-edge as a link. The URL hash holds the selected node id, so browser back and forward work.
- **Filters** combine (a node must pass all that are set): **FR** shows exactly the nodes that FR owns, the same set as `scripts/query.py fr <FR>`; **Timeline** shows that timeline's Stages and every node one edge away; **Source** shows the nodes decided by it; **Flow** shows the Flow and its path of Steps from the start Step through `next` links, with each Step's actor, stage, screen and rules. "Add one hop of context" widens any scope by one edge. **Neighbourhood** replaces the scope filters with the selected node and everything within 1 to 4 hops.
- **Start state:** the page opens on FR-005 (or the first FR), not on all 8,000+ nodes. "Whole graph" shows everything; it draws, but slowly at first, and reads as a dense cloud until you narrow it with type toggles or edge verbs. Deep links: `3d.html?fr=FR-005`, `?tl=main`, `?src=SRC-…`, `?flow=FLW-…`, `?ctx=1`, `?nbr=1&hops=2#NODE-ID`, `?all=1`.
- **Search** by id or title, as in the 2D viewer. A node outside the current filters is added to the picture when you open it.

Libraries (in `viewer/vendor/`, single-file builds, each with its licence): `3d-force-graph` 1.80.1 (published 2026-09-29; its bundle includes three.js r186 for its own drawing) and `three` 0.186.1 (published 2026-09-24; `three.min.js`, an IIFE build of `three.module.js` made with esbuild 0.28.2: `esbuild three-entry.js --bundle --format=iife --global-name=THREE --minify`, where the entry is `export * from 'three'`). The separate `three.min.js` is used only to draw the dashed derived edges, because the 3d-force-graph bundle has no dash option; the browser console shows one "Multiple instances of Three.js" warning for this. The library files were chosen at least two weeks after their release. To upgrade, rebuild with newer versions and replace the files in `vendor/`.
