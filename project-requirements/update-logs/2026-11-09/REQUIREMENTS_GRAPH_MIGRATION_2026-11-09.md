# Requirements Graph — Phase 4 PRD Migration (Overnight Run)

**Date:** 2026-11-09
**Type:** Major update — requirements graph population from the frozen PRD baseline
**Programme:** `plans/261108-1040-requirements-graph-programme/` (Hairline root), Phase 4
**Run log:** `plans/reports/orchestrator-261109-overnight-run.md` (Hairline root) — read its **Morning queue** before acting on anything below

## Summary

All 36 frozen FR PRDs in `archived/prd-baseline-2026-11-08/` were converted into graph change-sets by subagents (one per FR, Phase 4 checklist). 34 were applied overnight; the remaining two (FR-007B, FR-017) were applied on the morning of 2026-11-09 after the user took the decisions listed under "Morning decisions" below. **All 36 FRs are now in the graph.** No PRD text was edited; the PRDs stay the source of truth until the user approves `prd-structure.md`.

## What changed

| Area | Change |
|---|---|
| `graph/graph.db` | 60 change-sets applied (36 FRs plus one L04 fix). Export totals: 8205 nodes, 2866 fields, 1087 enum values, 13046 edges, 83 sources, 60 change-sets |
| `graph/graph.json` | Re-exported after each apply |
| `graph/changesets/` | 60 files: `2026-11-09-frNNN-<slug>[-partN].yaml`, one or more per FR |
| `graph/backups/` | One `graph-YYYYMMDD-HHMMSS.db` per apply step (pre-apply snapshot) |
| `graph/schema.yaml` | Rule and Screen id patterns now allow one optional letter after the FR number (`REQ-007B-001`, `SCR-007B-01`), matching the FR pattern |
| `graph/README.md` | New section "Headless review wrapper"; Setup and all commands now use `/usr/bin/python3`; aggregate-view convention noted under Database rules |
| `graph/checklists/migrate-fr.md`, `completeness-check.md` | Interpreter path updated; migrate-fr gains the dashboard-totals (aggregate view) row |
| `graph/scripts/headless_review.sh` | Interpreter now `${GRAPH_PY:-/usr/bin/python3}` |
| `graph/scripts/headless_review.sh` | New wrapper used for the OpenCode headless completeness checks |

## Morning decisions (2026-11-09, user)

1. FR-007B id format: widen the Rule and Screen id patterns rather than renumber. Applied.
2. FR-017 shared nodes (Payment, Payout, Commission entities; payment-reminder-timing Setting) stay owned by FR-007; FR-017 only adds to them. The `ENT-affiliate` create was converted to an update (FR-018 owns it); two duplicate enum values and nine duplicate edges dropped.
3. Dashboard totals with no Key Entity are modelled as aggregate-view entities (one per screen group, fields `calculated_by` their rule). Convention recorded in `migrate-fr.md`; ten such entities exist.
4. Interpreter: `/usr/bin/python3` is the documented route; the hook and `.ckignore` are unchanged.
5. FR-034 support-case events (assigned, admin reply, escalated) are produced by the Patient active stage; the three Provider-stage edges from FR-030 removed (`changesets/2026-11-09-fr034-support-case-event-producer.yaml`). L04 is now zero.
6. `prd-structure.md` approval and Phase 5 (schema v5) deferred to the next session.

## Applied

All 36 FRs: FR-001 to FR-007, FR-007B, FR-008 to FR-035, FR-037, FR-038.

## Lint state after the run

`lint.py` whole-graph: 4322 findings — L10 ×4144, L12 ×178. No L01 to L09, L11 or L13.

- L10 (no source) is expected until Phase 5 source back-fill runs.
- L12 near-duplicates and every other open item are consolidated in `plans/reports/review-queue-261109-0728-morning-queue-consolidated.md` (384 rows).

## Verification

- Each FR: dry run on a scratchpad copy, lint `--fr`, then live apply, lint `--fr`, whole-graph lint, export.
- FR-025 and FR-008 completeness checks passed (FR-025 via OpenCode DeepSeek paired with Sonnet, 87 % agreement; FR-008 via Sonnet after the headless run timed out).

## Notes for the maintainer

- Scripts run with `/usr/bin/python3` (system python with pyyaml) because the workspace hook blocks any command containing `.venv`. Confirmed by the user as the documented route.
- `scripts/migrate_schema_v5.py` was **not** run; schema stays v4 (id patterns widened only). Phase 5 is deferred to the next session.
- `prd-structure.md` (PRD compression template) awaits user approval; no PRD compression has been done.
- Nothing was committed.

## PRD structure approved (2026-11-09, later session)

- `graph/checklists/prd-structure.md` 0.1 proposal to 1.0: the user answered all seven questions. Compressed PRDs keep their reviewed wording, state each rule once, and tag field rows with graph field ids; Success Criteria, Assumptions, technical sections (after a re-check), Key Entities and open questions leave; Edge Cases stay; three pass checks (completeness, class list, FR position). Recorded as D35 in `plans/reports/advise-261105-0843-graph-model-decisions.md`.
- `graph/checklists/README.md` 1.3 lists `prd-audit.md` and `prd-structure.md`.
- Plan `plans/261108-1040-requirements-graph-programme/`: Phase 6 completed; Phase 9 re-scoped from rendering to compression with an FR-005 pilot; Phase 8 gains the PRD flow alignment check; Phase 5 records the missing Rule-to-Screen verb.
- Checklist set approved by the user (README 1.3, `migrate-fr.md` 1.1, `completeness-check.md` 1.1, `source-priority.md` 1.0, `prd-audit.md` 1.0, `prd-structure.md` 1.0, `agent-brief-template.md` 1.1); plan Phase 1 completed.

## Schema v5 applied (2026-11-09, later session)

User decision D38: a Rule can act on any object, not only a Stage, and a rule shared across FRs can be homed in the system PRD.

- `graph/schema.yaml` to version 5:
  - new verb `applies to` (Rule to Actor, Screen, Entity, Field or Event; any number per Rule);
  - new verb `references` (FR to Rule), for an FR that uses a Rule homed elsewhere;
  - new Rule attribute `scope: global`;
  - FR id pattern accepts `FR-SYS` (the system PRD) and Rule ids accept `REQ-SYS-NNN`.
- `graph/scripts/migrate_schema_v5.py` rebuilds the edge verb check. DB backed up to `graph/backups/graph-20261109-233301.db`, then migrated (user_version 5). No nodes or edges changed.
- `graph/scripts/lint.py`: L02 and L13 count `applies to` as well as `applies at` and skip global rules.
- Tests: 164 pass (`cd graph/scripts && /usr/bin/python3 -m unittest -q`); new tests cover `applies to`, global scope and FR-SYS homing.
- Lint unchanged at 4,322 findings (L10 4,144, L12 178). Export regenerated: 8,205 nodes, 13,046 edges.
- Checklists: `migrate-fr.md` and `completeness-check.md` to 1.2 (fill `applies to` links; `cited` needs a `references` edge); README to 1.4. `migrate-fr.md` also loses a dedup step that named an invalid `shows` edge to a Rule.
- The Phase 5 schema gap (no Rule-to-Screen link) is resolved; links are filled as the completeness checks run.
- Review queue routing and lint (D40, same session): Rule gains optional `distinct_from` (pairs reviewed and kept apart; L12 skips them; no DB change, schema stays at version 5). L02 now fires only when a Rule's placing edges all end at retired nodes; a Rule with no edge is L13 only. Lint total unchanged at 4,322; 165 tests pass. `completeness-check.md` 1.2 also rules on the FR's kind B and C queue rows. Queue rows E1 to E8, E10, F1 to F8 and F10 closed with evidence; 364 rows routed to the D37 steps and a product-owner list.
- Model decisions D41 (same session): schema v6 will add a Flow node (ordered steps pointing at Stage, Screen, Rules; flow wording stays in the PRD) before the 34 completeness checks; filter, search and sort criteria are Rules that `applies to` the Screen, translation keys stay out; user stories stay PRD text and cite their Flow; partial and missing rows are fixed right after each FR's check. E9 fixed in `migrate-fr.md` 1.2 (pass condition allows listed L12 pairs).

## Related

- Previous: `update-logs/2026-11-08/REQUIREMENTS_GRAPH_FREEZE_2026-11-08.md`
- Agent reports: `plans/reports/docs-manager-261109-fr*-migration.md` (36), `plans/reports/tester-261109-*.md`
