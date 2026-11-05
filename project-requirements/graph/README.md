# Requirements graph

This folder holds the requirements graph. It stores FRs, stages, actors, entities, fields, rules, events, settings, screens and sources as nodes, and the typed edges between them. `graph.db` (SQLite) is the only place graph data lives. `schema.yaml` defines the node types, the attributes each type allows, the ID pattern for each type, the edge verbs with the node-type pairs they may join, and the closed value lists.

## Contents

- `schema.yaml`: the graph schema. Changing node types, verbs or enum values counts as a schema migration, so back up `graph.db` first.
- `graph.db`: the graph database. It has six tables: `nodes`, `fields`, `enum_values`, `edges`, `sources` and `changes`.
- `scripts/common.py`: loads and validates `schema.yaml`, and opens the DB with foreign keys enforced.
- `scripts/init_db.py`: creates an empty `graph.db`.
- `scripts/test_init_db.py`: tests for the schema loader and the database rules.
- `backups/`: dated copies of `graph.db`, written before it is replaced.

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

## Setup

Run these from this folder. System pip is blocked by PEP 668, so use the local virtual environment:

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

## Create the database

```bash
.venv/bin/python scripts/init_db.py                # creates graph.db here
.venv/bin/python scripts/init_db.py path/to/x.db   # or at another path
.venv/bin/python scripts/init_db.py --force        # replaces graph.db after copying it to backups/graph-YYYYMMDD-HHMMSS.db
```

Without `--force`, the script will not overwrite an existing database. `--force` replaces the database with an empty one, so all graph data is lost unless you restore the backup.

## Write and query

`scripts/write.py` is the only way to change the graph. It applies one change-set file (JSON for `.json`, YAML otherwise) in a single transaction. A change-set has `reason`, `by`, an optional `source_id` (a Source node), and a list of `operations`: `add_node`, `update_node`, `retire_node`, `add_field`, `update_field`, `add_enum_value`, `retire_enum_value`, `add_edge`, `remove_edge` and `add_source`. The keys of each operation are listed at the top of the script. When `add_enum_value` has no `sort_order`, the value goes after the field's current values (highest `sort_order` plus one, or 0 for the first). Every operation is checked against `schema.yaml` first; if any check fails, nothing is written and each problem is printed with its operation index, such as `operations[3] (add_edge): ...`. Each applied change-set adds one `changes` row per attribute changed, all under one generated `changeset_id`, and raises `version` by one on every existing node it touched. Exit codes: 0 applied, 1 change-set invalid, 2 database error.

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
.venv/bin/python scripts/write.py changes/add-quote-expiry.yaml
```

`scripts/query.py` only reads. It prints a plain table, or JSON with `--json`, and takes `--db PATH`. Subcommands: `impact <node-id> [--depth N]` (everything within N hops through any edge, default 2), `lifecycle <timeline>`, `cites <node-id>`, `fr <FR-id>`, `history <node-id>`, `at <node-id> <ISO-timestamp>` (attributes at that time; a timestamp without an offset is read as UTC) and `changeset <changeset-id>`.

```bash
.venv/bin/python scripts/query.py impact SCR-004-01 --depth 2
```

Tests: `.venv/bin/python scripts/test_write_query.py`.

## Lint, export and render

These three scripts only read the database. Each takes `--db PATH` to use a DB other than `graph.db`.

`scripts/lint.py` checks every active node against the guardrails (rules L01 to L11, listed at the top of the script). It prints one row per finding, or `--json`, and exits 1 if there is any finding, 0 if the graph is clean, 2 on an error. Each finding ID is the rule code plus its subject, such as `L03:SCR-004-01`, so counts can be compared between runs. `--fr FR-004` limits the check to nodes that FR owns.

```bash
.venv/bin/python scripts/lint.py --fr FR-004
```

`scripts/export.py` writes `graph.json` for the viewer: active nodes, fields, enum values, edges and sources, each list sorted so the file diffs cleanly. `--include-retired` adds retired nodes. History is summarised in a top-level `changes` array, one entry per change-set newest first (`id`, `at`, `changed_by`, `reason`, `source_id`, the sorted `nodes_added` and `nodes_updated` ids, `edges_added`, `edges_removed` and `rows`), which the viewer's Changes tab lists; individual change rows stay in `graph.db`.

```bash
.venv/bin/python scripts/export.py                 # writes graph.json here
```

`scripts/render.py` renders the graph-owned sections of one FR PRD as markdown: Scope, Actors, Workflows, Screen Specifications, Business Rules, Data, Events, Settings, Dependencies, Sources and Change Log. Rules owned by another FR appear only as a `[REQ-NNN-NNN] title` citation. The output is derived, so hand edits are lost on the next render.

```bash
.venv/bin/python scripts/render.py FR-004 --out /tmp/fr-004.md   # stdout without --out
```

Tests: `.venv/bin/python scripts/test_lint_export_render.py`.

## Change-set files and replay

Files under `changesets/` are kept so a change-set can be reviewed before and after it is applied. They are a record, not a rebuild script: each one was validated against the schema version in force when it was written, so a later schema change (for example a new required attribute) can make an older file fail on a fresh database. Recovery is from `backups/`, and history is the `changes` table in `graph.db`. Do not edit an applied change-set file to make it replay.

## Run the tests

```bash
.venv/bin/python scripts/test_init_db.py
```

The tests use temporary databases. They never touch `graph.db`.

## Viewer

`viewer/index.html` is a read-only review page for `graph.json`. Use it to check what a migration batch added. It has three parts. **Timelines** shows one lane per timeline, the `follows` order, the `enters from` and `joins` links between lanes, and the actors in each stage. **By FR** lists each FR's owned rules, entities with their fields and enum values, events, settings and screens. The **node panel** shows a node's attributes and its in-edges and out-edges. A search box finds nodes by id or title. The page works offline and needs no build step.

Run `scripts/export.py` first so `graph.json` is current. Then, from this folder:

```bash
python3 -m http.server 8765
```

and open http://localhost:8765/viewer/ . You can also open `viewer/index.html` straight from disk. The browser will block the automatic load, so drop `graph.json` onto the page or pick it with the file picker. The URL hash holds the selected node id (for example `#STG-main-06-treatment`), so browser back and forward move between the nodes you have opened.
