# Checklist: migrate one FR PRD into the graph

Version: 1.1 (2026-11-09)

## Purpose
Turn one frozen FR PRD into a change-set file that loads every business requirement of that PRD into the graph as nodes and edges with provenance, without rewriting any requirement and without dropping any.

## Inputs
- The frozen PRD: `archived/prd-baseline-2026-11-08/frNNN-slug/prd.md` (project root; read-only). Never migrate from the live copy.
- Not an input: the FR's Change Request files. The PRD holds every requirement; a CR only records what changed between PRD versions (D14). Do not read CRs during migration.
- `project-requirements/graph/schema.yaml` (node types, id patterns, verbs, enums) and `graph/README.md` (write.py operations).
- Current graph state: `/usr/bin/python3 scripts/query.py fr FR-NNN`, plus `query.py impact <id>` and `query.py cites <id>` for nodes other FRs already created as stubs.
- `project-requirements/sources/source-register.md` and the meeting notes it links, for `decided by` edges.
- `checklists/source-priority.md` for conflicts between sources.
- The decisions note `plans/reports/advise-261105-0843-graph-model-decisions.md` (D1 to D30) for model rules. The two earlier migration reports (`plans/reports/docs-manager-261105-fr004-migration.md`, `-fr005-migration.md`) show the expected depth and the report shape.

## Outputs
- One change-set file `graph/changesets/YYYY-MM-DD-frNNN-slug.yaml` (`reason`, `by`, `operations`; see README). Not applied by the migration agent: the controller applies it after backup.
- A migration report at the path given in the brief, with the sections listed under "Report" below.

## Steps

### 1. Prepare
1. Re-read this checklist and `source-priority.md`.
2. List the PRD headings with `rg -n "^#{1,4} " <prd>` and read the PRD in section ranges, every section, in order. Files over 1000 lines are read in ranges, never whole.
3. Run `query.py fr FR-NNN` and note every node already owned by this FR (stubs created by earlier FRs). Those are updated with `update_node` or `update_field`, never recreated.

### 2. Map each PRD section to the graph
Walk the PRD top to bottom. Every line that states something the product must do, show, store, allow or forbid is a business requirement and must end up as a node, a field, an enum value, an edge attribute, or an explicit "not migrated" entry in the report.

| PRD section | Graph target | Notes |
|---|---|---|
| Executive Summary | none (hand-written in render, D13) | Promote any rule hidden here. |
| Module Scope, Multi-Tenant Breakdown | Rule nodes for scope statements; `acts in` edges Actor to Stage | Per-platform scope lines usually hide rules ("providers see acceptance outcomes read-only"). |
| Communication Structure | Event nodes, `emits` edges; Rule nodes for notice content | |
| Entry Points | Rule node (one per FR, "entry points to ...") and `uses` edges Actor to Screen | |
| Business Workflows, Main Flow | `applies at` for every rule involved; Stage `reads` and `writes` Entity; `emits` Event | Each numbered step that states an outcome or check becomes or joins a Rule. |
| Alternative Flows, Edge Cases | Rule nodes | Each alternative with a distinct outcome is a rule. |
| Screen Specifications | Screen node (`SCR-NNN-NN`, `platform`, `description`), `belongs to` Stage, `uses` from Actor, `shows` edge to a Field with required `provenance` and optional `label`, `editable` | Screens own no fields (D15). UI controls (buttons, tabs, modals) are not fields; their behaviour becomes a Rule or part of the screen description. A screen field with no Entity field is an orphan: add the Field on the owning Entity (stub Entity owned by the true FR if needed) and say so in the report. |
| Business Rules | Rule nodes; existing REQ ids kept verbatim; prose rules get the next free `REQ-NNN-NNN` | Statement text is copied, not paraphrased. Rationale bullets that restate a rule merge into its `rationale`. |
| Settings, configurable values | Setting node owned by the FR the PRD names (often FR-026), `governed by` edges from the Rules it controls | |
| Key Entities | Entity nodes, Field nodes (`add_field`: name, data_type, required, calculated_by), enum values | Field names are immutable: rename only by retiring and adding. Calculated fields point at the Rule that computes them. |
| Dashboard totals (counts, sums, rates shown on a screen but owned by no Key Entity) | One Entity per screen group, marked in its description as an aggregate view that is not stored; one Field per total, each `calculated_by` the Rule that defines it; `shows` edges from the Screen | Convention approved 2026-11-09 (examples: `ENT-installment-plan-metrics`, `ENT-help-centre-stats`, `ENT-analytics-metrics-aggregate`). List the entity in the report as agent-introduced. |
| Dependencies (internal) | No nodes. Listed in the report as cross-FR citations with PRD line numbers | A rule stated here that the other FR does not own becomes a Rule here. |
| Dependencies (external, data) | Report only | |
| Assumptions | Rule only when the assumption is in fact a business rule; otherwise report "not migrated" | |
| Implementation Notes, Integration Points, Scalability, Security mechanics | Not migrated (technical spec), after promoting any business rule inside them | Idempotency, audit, concurrency and version-validation statements are business rules. |
| Success Criteria, User Stories, Glossary, Approvals, Change Log | Not migrated (no node type) | List in the report so the completeness check can mark them "no node type" instead of "missing". |

Rules for every node:
- One owning FR. Ownership follows the PRD; boundary disputes are recorded as a question, not fixed (standing rule 3, D10).
- Every Rule `applies at` one or more Stages (default: the stage this FR acts in; add others only when the PRD says so).
- Every Rule and sourced Entity gets a `decided by` edge when a source item covers the topic (see step 4). Rules without a source stay without one; L10 records the gap.
- Every Event has one producer Stage. When the PRD fires the same event at two stages, record the first and raise it as a question (carried item D7).
- Nodes owned by another FR that this PRD needs (an entity this screen shows) are created as stubs owned by their true FR, with only the fields this PRD shows.
- IDs follow `schema.yaml` patterns and never change once written.

### 3. Dedup before every Rule (Phase 3 mechanism)
Before writing an `add_node` for a Rule, check whether the graph already holds the same rule:
1. Run the duplicates query from Phase 3 (`query.py duplicates --text "<candidate statement>"`; until Phase 3 lands, search `graph.json` for the key phrase with `rg -n -m 10`).
2. Same rule already exists, any owner: do not add a node. Add the missing edges to the existing Rule (`applies at`, `shows` from this FR's screen, `governed by`). If the owner is another FR, list the pair in the report under "Cross-FR duplicates" with your ownership recommendation (the FR whose stage it applies at first, Phase 3 rule).
3. Near-duplicate (same meaning, different wording): add the node, and list the pair under "Possible duplicates" for the L12 lint and the user. Never silently merge text.
4. This PRD repeats its own rule under two screens: one Rule, two `shows` or `applies at` edges.

### 4. Provenance
1. For each Rule and sourced Entity, find the meeting item or brief item that decided it (`SRC-MTG-00N-xxx`, `SRC-DOC-001-xxx`), using the PRD References section, the PRD Change Log and the source register. Add `decided by`.
2. Apply `source-priority.md` when sources disagree. Never pick a winner yourself; write the conflict up.
3. Set the change-set `source_id` only when one source covers the whole change-set; otherwise leave it out and let edges carry provenance.

### 5. Write the change-set
1. Operations in dependency order: `add_node` for Entities before `add_field`; Rules before `calculated_by` references; Screens before `shows`; Settings before `governed by`.
2. Skip any edge that already exists (check with `query.py impact` or the export); write.py rejects duplicates and the whole file fails.
3. Do not run `write.py` against `graph.db`. Validate against a copy if you need to: `cp graph.db /tmp/x.db && /usr/bin/python3 scripts/write.py <file> --db /tmp/x.db` (check README for the exact flag), then `lint.py --db /tmp/x.db --fr FR-NNN`.

### 6. Report
Sections, in this order: checklist path and version; change-set file and operation counts by op; nodes created by type (owned by this FR, owned by another FR, total); edges by verb; ownership decisions; new REQ ids assigned (REQ, title, PRD location); fields added for orphan screen fields; cross-FR citations (FR, PRD lines, content); cross-FR duplicates and possible duplicates; not migrated (section, reason); lint findings expected; needs product owner decision (numbered, plain language, per `source-priority.md` "unclear item" format); status line.

## Pass condition
- Every PRD section appears in the mapping, the report's "not migrated" list, or the cross-FR citations.
- Every REQ id in the PRD exists as a Rule node id in the change-set or already in the graph.
- Every screen field maps to a Field (`shows` edge with provenance) or is listed as a UI control.
- Every Key Entities field exists as a Field.
- Change-set validates on a DB copy with exit 0; lint on the copy shows no new L01 to L09, L11 to L13 for this FR.
- Report has all sections and a status line.

## Stop and ask when
- Two sources, or the PRD and a source, state different rules for the same topic (write the item up; do not choose).
- A rule's owner is unclear and the choice changes another FR's scope.
- A field in Key Entities has a name that collides with an immutable existing field of different meaning.
- A PRD line is business-nonsensical or contradicts another line of the same PRD (the FR-005 line-561 case). Record both readings.
- The PRD depends on an FR or document that does not exist in the repo.
- Operation count would exceed what one change-set can be reviewed as (over about 600 operations): split by PRD section and say so.

## Change log
- 1.0 (2026-11-08): first version, built from D1 to D30 and the FR-004/FR-005 migration reports. Dedup step references the Phase 3 duplicates query; until Phase 3 lands, use the `rg` fallback in step 3.
- 1.1 (2026-11-09): CRs removed from inputs, steps and report on user decision; the PRD is the only migration source. Provenance uses the PRD References and Change Log instead of CR Decision evidence.
