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

## Related

- Previous: `update-logs/2026-11-08/REQUIREMENTS_GRAPH_FREEZE_2026-11-08.md`
- Agent reports: `plans/reports/docs-manager-261109-fr*-migration.md` (36), `plans/reports/tester-261109-*.md`
