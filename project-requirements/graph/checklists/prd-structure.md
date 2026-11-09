# Checklist: PRD structure (compressed PRD)

> v1.0 — approved by the user on 2026-11-09 (answers to the seven proposal questions are under "Decisions"). The audit figures under "Evidence" are as of 2026-11-09 and are not kept current.

Version: 1.0 (2026-11-09)

## Purpose
State what a compressed PRD contains and how compression is checked. Phase 9 compresses each reviewed PRD against this checklist; the graph proves nothing was lost and links shared fields, it does not write the PRD.

## Inputs
- The 38 audit reports `plans/reports/docs-manager-261109-prd-audit-fr*.md` (classes and duplicate values per heading, produced under `prd-audit.md` v1.0) and the consistency check `plans/reports/docs-manager-261109-prd-audit-check.md`. Stateful records; the figures below are as of 2026-11-09 and are not kept current.
- `graph/schema.yaml` node types: FR, Stage, Actor, Entity, Field, Rule, Event, Setting, Screen, Source.
- `prd-audit.md` content-class list (the vocabulary below).
- Not an input: the live PRDs, or any decision about removal. None exists yet.

## Evidence from the audit (observations)
Figures cover 38 PRDs, 43,803 lines, 2,409 headed sections. Line share is the share of all lines; "median" is the median per-PRD share. Primary class only (see wording issue b in the check report). Per-FR values are in the check report's totals table.

### Classes present in every PRD (38 of 38)
| Class | Share of all lines | Median per PRD | Graph node type |
|---|---|---|---|
| flow | 15.1% | 14.6% | Stage (partly), Rule; no direct type |
| rule | 9.1% | 9.2% | Rule |
| scope | 4.4% | 4.2% | none (summary text; migrate-fr maps scope statements to Rule) |
| dependency | 4.3% | 4.1% | none (cross-FR references; no node type) |
| other (mostly container headings, front matter) | 4.8% | 4.8% | none |
| success metric | 2.8% | 2.8% | none |
| assumption | 1.8% | 1.8% | none |
| CR history | 1.7% | 1.6% | none (Source is for meeting and document sources, not change logs) |
| approval | 1.3% | 1.4% | none |

### Classes present in nearly every PRD
| Class | PRDs | Share of all lines | Graph node type |
|---|---|---|---|
| screen | 36 | 35.6% (median 28.8%, range 0 to 69.6%) | Screen (plus Field via `shows`) |
| user story | 37 | 6.9% | none |
| technical note | 36 | 3.6% | none (migrate-fr notes rules hide here) |

### Classes present in few PRDs
| Class | PRDs | Share of all lines | Graph node type |
|---|---|---|---|
| field | 17 | 4.1% (up to 28.8% in one PRD) | Field |
| actor | 15 | 1.1% | Actor |
| setting | 13 | 1.0% | Setting |
| repetition | 12 | 1.5% | none (restates other sections) |
| event | 7 | 0.7% (up to 18.3%) | Event |
| open question | 8 | 0.1% | none |
| glossary | 1 | under 0.1% | none |
| entity (unlisted label, 2 reports) | 2 | 0.1% | Entity |

### Other observations
- Rows whose Duplicate value contains `graph`: about 28,700 lines (65.6% of all lines), of which screen is about half. The flag is applied unevenly by readers (see the check report), so treat as an upper bound on content the graph can hold.
- Rows marked `same PRD`: the same facts appear under another heading of the same PRD for most screen, rule, flow and scope lines.
- Rows marked `none` (content only in that section): 3,259 lines, 7.4% of all lines.
- Classes with no node type (user story, dependency, success metric, assumption, approval, CR history, technical note, scope) together make up roughly 27 percent of lines.
- Several of these classes carry rules in hidden form (technical note, edge cases, scope), per the audit notes and `migrate-fr.md`; whether a class is "safe" to move depends on the migration having captured them.


## Decisions (user, 2026-11-09)
Model: the compressed PRD is the existing reviewed PRD with redundancy removed (D33). The PRD keeps its wording; the graph checks coverage and links shared items. Nothing is generated from the graph.

| # | Question | Decision |
|---|---|---|
| Q1 | How do node-type classes (screen, field, rule, event, setting, actor) appear? | Keep the PRD wording and the scope of each rule as written now. Each rule is stated once; any other place that restated it cites the REQ id instead. Every field-table row gets its graph field id in the row (for example `(ENT-subquote.offered_price)`), so one field repeated on several screens is visibly the same field and the graph lists every screen that shows it. A grouped row (for example "Subquote Summary") is tagged with its entity id or a list of field ids. |
| Q1b | Same field described on several screens of one PRD | Keep each screen's row and wording; the shared graph id shows it is one field. |
| Q2 | Classes with no node type | Drop Success Criteria (success metrics) and Assumptions; they stay in the frozen baseline. Keep user stories and scope. Dependencies become one short list of related FR ids. Open questions are resolved or moved to the review queue, then removed. |
| Q3 | Flows | Keep flow text as it is. Separately, check each FR's flows against the graph's system-wide stage sequence and cross-FR handoffs; mismatches go to the user as decisions, flows are not edited by the check. |
| Q4 | Repetition | Remove by class once the source section is confirmed present; the pass checks below catch any loss. No per-item sign-off. |
| Q5 | Hidden rules | Edge Cases stay in the PRD; they are business rules. Technical sections (Implementation Notes and similar) leave the PRD under D34, but only after a completeness re-check of that section; any business rule found there moves into Business Rules in its original wording first. |
| Q6 | Pass rule | Three checks, all required: line-by-line completeness, the class list, and the FR position check (see Pass condition). No line-count target. |
| Q7 | Change Log and Approvals | Keep both. The Change Log restarts with one first entry pointing to the frozen baseline `archived/prd-baseline-2026-11-08/`; the Approvals block is kept short. Earlier history stays in the archive. |

## Content classes in a compressed PRD
| Class (audit vocabulary) | In the compressed PRD | Notes |
|---|---|---|
| scope (Executive Summary, Module Scope, Entry Points) | Keep | Wording as is; repetition inside it removed by class |
| flow (Business Workflows) | Keep as is | Subject to the flow alignment check (Q3) |
| screen | Keep | Wording as is |
| field | Keep, tagged | Graph field id in every row (Q1, Q1b) |
| rule (Business Rules, Functional Requirements Summary, screen rules) | Keep, stated once | Repeats replaced by a REQ id citation (see Steps 3) |
| edge case | Keep | Business rules (Q5) |
| actor, event, setting | Keep | Wording as is |
| user story (User Scenarios and Testing) | Keep | |
| glossary | Keep where present | |
| dependency | Reduce | One list of related FR ids; external, data and technical dependencies leave with the technical sections |
| success metric | Drop | Frozen baseline only |
| assumption | Drop | Rules stated inside are moved to Business Rules first |
| technical note (Implementation Notes and similar) | Drop after re-check | D34; Q5 |
| Key Entities | Drop | D34; Entities stay in the graph |
| open question | Drop | Resolved or moved to the review queue first |
| repetition | Drop | Q4 |
| CR history (Change Log) | Keep, restarted | Q7 |
| approval | Keep, short | Q7 |

## Steps (per FR)
1. Start from the reviewed PRD in `functional-requirements/frNNN-*/prd.md`, never from the graph.
2. Re-check every section that will be dropped (technical notes, assumptions, success criteria, dependency text, open questions) with `completeness-check.md`; move any business rule found into Business Rules in its original wording.
3. Rules stated more than once: keep the fullest wording verbatim where it stands; replace each other occurrence with a one-line citation of its REQ id. If a shorter occurrence adds any condition, actor, value or exception, it is not a repeat: keep it and list it in the report.
4. Tag every field-table row with its graph field id from `query.py fr FRNNN` and the screen's `shows` edges. A row with no matching field is listed in the report, not invented.
5. Remove the dropped classes and repetition; reduce Dependencies to the FR id list; restart the Change Log with the baseline pointer.
6. Run the three pass checks below and write the report.

## Outputs
- The compressed PRD in place (after the user approves that FR's report).
- `plans/reports/docs-manager-YYMMDD-frNNN-compression.md`: removed sections by class, rule citations made, field rows tagged and untagged, the three pass results, and items needing a user decision.

## Pass condition
1. Line-by-line completeness: every business line of the frozen PRD (`archived/prd-baseline-2026-11-08/`) is present in the compressed PRD, or its removal falls under a dropped class or a repetition whose source survives. Zero missing, zero partial.
2. Class list: only the classes marked Keep, Keep tagged, Keep stated once, Reduce, Keep restarted or Keep short above remain.
3. FR position check: the compressed PRD gives the same picture of the FR on its own and in the whole system as before compression. Its flows, entry points, screens and stages match the graph (`query.py fr`, `query.py lifecycle`), and its handoffs to other FRs and its dependency FR list match the graph's cross-FR edges. Compression must not change what the FR owns, where it sits in the timeline, or which FRs it hands over to.

## Flow alignment check (Q3)
Runs per FR, independent of compression: compare each Business Workflows flow (main and alternative) with the graph's stage sequence for the timelines the FR acts in and with its cross-FR edges. Report steps that skip, reorder or contradict a stage, handoffs to an FR the graph does not link, and graph links the flow never mentions. Findings are user decisions; the check does not edit flows or the graph.

## Stop and ask when
- A business line would be removed and no rule above covers its removal.
- A restated rule differs in substance from its fullest wording.
- The FR position check or the flow alignment check finds a change or a mismatch.
- A field row has no graph field, or a graph field shown on the screen has no row.

## Change log
- 0.1 (2026-11-09): proposal drafted from the 38 audit reports; no criteria approved.
- 1.0 (2026-11-09): user answered Q1 to Q7 plus follow-ups (field id tags, repeated field rows, dependencies and open questions, technical-section re-check, FR position check); content-class table, steps, outputs and pass condition fixed.
