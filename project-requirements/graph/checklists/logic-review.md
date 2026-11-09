# Checklist: FR logic review

Version: 0.1 draft (2026-11-10), not approved

> **Draft for user approval.** Nothing runs under this checklist until the user approves it. Drafted under D43 item 6 from the procedure the user approved as D39 (`plans/261108-1040-requirements-graph-programme/phase-10-final-logic-review.md`). Items marked **Open for approval** are drafting choices the phase file leaves open; they are listed together under "Open for approval" at the end.

## Purpose
Review one FR as a whole for anything illogical (contradictions, dead ends, unreachable states, gaps at FR boundaries), with a written verdict and evidence for every item of the FR. A review counts only if a script finds every manifest item answered with evidence and every planted test defect reported. Nobody who reviews, fixes or coordinates can declare an FR clean; clean is the exit rule below plus the user's reading.

## Roles
- **Controller** (main session): builds the review copy and manifest, plants and seals the test defects, runs the gate, routes findings, keeps the findings ledger. Never marks an item OK and never rejects a finding alone.
- **Reviewer A** (fresh agent each round, Sonnet or Opus, no history): one verdict row per manifest item, plus the scenario walkthroughs.
- **Reviewer B** (a different fresh agent, Sonnet or Opus): adversarial; attacks A's OK verdicts in the high-risk classes and runs scenarios A did not.
- **Fixer** (separate agent): writes the change-set and PRD edit for each accepted finding. Never reviews its own fix.
- **User**: decides product questions, approves rejections where needed, reads each FR's final report.

What reviewers are told: that defects were planted in their copy. Never how many, where, of which kind, the previous round's verdicts, an expected result, or a target number.

## Inputs
For reviewers (their whole read path; the brief names these exact files):
- This checklist.
- The manifest in Markdown (`manifest.md`) for the round.
- The review copy: `copy/graph.db` (query with `scripts/query.py --db <copy>` and `scripts/lint.py --db <copy>`) and `copy/prd.md`.
- `graph/schema.yaml` (node types and verbs).
- `checklists/source-priority.md` (which source wins) and the "Flow alignment check" section of `checklists/prd-structure.md`.
- Neighbour FRs' PRDs, read by section, only for the boundary items (Q11).

Reviewers do not open `graph/graph.db`, `graph/graph.json`, the original PRD, the gate output, the sealed defect file, or any earlier logic-review report.

For the controller: the phase file, `scripts/logic_manifest.py`, `scripts/logic_gate.py`, `checklists/completeness-check.md` (re-check after fixes), `checklists/agent-brief-template.md`.

## Logic classes and their questions
Each class has one question. A finding names the question it answers (Q1 to Q11) in its row's Note.

| Code | Class | Question | Where to compare (graph) |
|---|---|---|---|
| Q1 | Contradiction | Do two rules contradict each other, or does a rule contradict a setting default? | Rule statements that act at the same Stage or `applies to` the same object; `governed by` Setting defaults and units |
| Q2 | Reachability | Is there a status or stage that cannot be reached, or that cannot be left? | Stage `follows`, `enters from`, `joins`; Step `at` and `next`; enum values of status Fields and the Rules that set them |
| Q3 | Actor coverage | Is there an action with no actor allowed to do it, or an actor allowed something the FR forbids elsewhere? | Step `done by`; Actor `acts in` and `uses`; Rules `applies to` an Actor |
| Q4 | Rule placement | Is there a rule with no place it acts (no stage, no `applies to`, not global)? | Rule `applies at`, `applies to`, `scope: global`; Step `applies` |
| Q5 | Data flow | Is there a field written but never read, read but never written, or shown with no source? | Stage `reads` and `writes`; Screen `shows` with its provenance; Field `calculated by` |
| Q6 | Events | Is there an event emitted with no consumer, or consumed with no producer? | Stage `emits`; Rules `applies to` the Event; PRD lines naming the event as a trigger (the graph has no consume verb) |
| Q7 | Time and money | Are thresholds, windows, currencies and rounding consistent within the FR and with every FR it touches? | Setting default and unit; Rule statements with numbers, durations, currencies, rounding; the same values in neighbour FRs |
| Q8 | Permissions and visibility | Are permissions and data visibility consistent across actors? | Actor `uses` Screen; Screen `shows` Field; Rules `applies to` Actor, Screen or Field |
| Q9 | Edge cases | Is there an edge case named in the PRD with no rule that handles it? | PRD Edge Cases and alternative flows against Rules and Steps |
| Q10 | Terms | Is the same thing called by different terms across the FR or its neighbours? | Titles of Entities, Fields, enum values, Stages, Events; PRD wording; neighbour PRDs |
| Q11 | Boundary | Does what this FR hands to and receives from each neighbour FR match the neighbour's side? | Boundary edges; cross-FR `next`; Step `handoff_to` and `handoff_from`; `references`; the neighbour PRD's matching section |

Which questions each manifest item gets at least:

| Item kind | Questions |
|---|---|
| PRD section | Every question its lines touch; Q9 and Q10 always |
| Rule | Q1, Q4, Q7, Q9 |
| Setting | Q1, Q7 |
| Stage | Q2 |
| Actor | Q3, Q8 |
| Entity, Field | Q5, Q8, Q10 |
| Event | Q6 |
| Screen | Q5, Q8 |
| Step | Q2, Q3, and its place in the scenario walkthroughs |
| Source | Whether the rules decided by it follow it (`source-priority.md`) |
| Boundary edge, neighbour FR | Q11, Q7, Q10 |
| Flow | Q2, Q11, and its scenario walkthrough |

## Checks reused from other checklists
- `completeness-check.md` (v1.3): after each fix is applied (step 7), the controller has the PRD lines the fix touched re-checked line by line, so fixes do not reopen a gap between PRD and graph. The FR does not enter the next round until those rows are `landed`.
- `source-priority.md` (v1.0): when a finding is two sources or a source and the PRD disagreeing, the trust order decides which side is wrong; a finding that needs a business reading is written in its "Unclear item format" and goes to the user.
- `prd-structure.md` (v1.0), "Flow alignment check": run on every Flow walkthrough; a step that skips, reorders or contradicts the Stage order, or a hand-off to an FR the graph does not link, is a finding (Q2 or Q11).

## Procedure, per FR, per round
1. **Review copy and planted defects (controller).** Make a fresh round folder in the session scratchpad: `logic-review/FR-NNN/rN/copy/` holding a copy of `graph.db` and of the PRD under review (**Open for approval:** the PRD is the frozen baseline, which the manifest script defaults to, or the live compressed PRD after Phase 9). Plant 3 to 5 defects, drawn in rotation from the kinds below, at least one a one-word change, all different from earlier rounds:
   - contradicting threshold across FRs;
   - reversed word (before/after, minimum/maximum, may/must);
   - removed link;
   - unreachable stage;
   - actor permission swap.
   Graph defects are made with direct SQL on the copy, not with `write.py`, so the copy's change history does not show them (**Open for approval**). Prefer defects that `lint.py --db <copy>` does not report (**Open for approval**). Record each defect in the sealed file (format below) in `logic-review-sealed/FR-NNN-rN.json`, a scratchpad folder outside the round folder. The real graph and PRDs are never touched.
2. **Manifest (script).** Build it on the copy, after planting (**Open for approval:** the phase file lists the manifest first; built from the unplanted graph, a removed link would still be a manifest row and give the defect away):
   ```
   /usr/bin/python3 scripts/logic_manifest.py FR-NNN --db <round>/copy/graph.db --prd <round>/copy/prd.md --out <round>/manifest.json
   /usr/bin/python3 scripts/logic_manifest.py FR-NNN --db <round>/copy/graph.db --prd <round>/copy/prd.md --format md --out <round>/manifest.md
   ```
   The manifest lists every item; the reviewer does not choose what to look at. Its item ids are stable across rounds, so the ledger can count findings per item (repeat rule).
3. **Review A.** Brief per `agent-brief-template.md`, pointing at this checklist and the inputs above. The reviewer writes the report in the format below: a verdict row for every manifest item, the scenario walkthroughs, the findings list, and the "Not checked or could not verify" section.
4. **Gate (script).**
   ```
   /usr/bin/python3 scripts/logic_gate.py --manifest <round>/manifest.json --report <report> --defects <sealed file>
   ```
   Exit 0 pass, 1 void, 2 bad input. A void report is never patched: a new reviewer A reruns the round on the same copy and manifest. Record the planted-defect recall the gate prints. The gate output is never shown to a reviewer.
5. **Review B (adversarial).** A different fresh agent receives A's report and the same copy. It attacks every OK verdict in A's report on the high-risk items (below) and runs at least two scenarios A did not. Anything B finds is recorded as a miss by A.
6. **Triage (controller with reviewer B and the user).** Each finding gets one outcome:
   - **fix**: goes to the fixer;
   - **user decision**: written in `source-priority.md` unclear-item format and sent to the user;
   - **rejected**: only with evidence plus agreement from reviewer B.
   Nothing is closed as minor or out of scope without the user. **Repeat rule:** when the same manifest item draws a finding for the third time, or the FR has findings in a third round, it stops and waits for the user's decision; no further fix or rejection on it until then.
7. **Fix.** The fixer writes a change-set and the matching PRD edit, each citing the finding (`FR-NNN rN F<n>`). The controller backs up `graph.db`, applies the change-set, then has the touched PRD lines re-checked under `completeness-check.md`.
8. **Next round.** Repeat from step 1 on the whole FR, not only the changed lines, with fresh reviewers and new planted defects.

## High-risk items for reviewer B
B attacks every row A marked OK whose item is: a boundary edge, a neighbour FR, a Flow, a Step, a Stage, an Actor, a Setting, or a Rule. These carry the money, time, permission, status-change and boundary logic the phase file names; Rules cannot be sorted into those classes mechanically, so all are attacked (**Open for approval:** the alternative is that B selects the rows itself, which lets the reviewer choose what to look at).

## Report format (reviewer A)
Path: `plans/reports/tester-YYMMDD-frNNN-logic-review-rN.md`. The gate parses the parts marked (gate).

```
# FR-NNN logic review, round N, reviewer A

Checklist: project-requirements/graph/checklists/logic-review.md v0.1
Manifest: <round>/manifest.md (generated <timestamp>)
Review copy: <round>/copy/graph.db, <round>/copy/prd.md (N lines)

## Verdicts

| Item | Verdict | Evidence | Note |
|---|---|---|---|
| S:business-workflows/main-flow | OK | prd:85-104 against STP-005-001, STP-005-002, STG-main-03-accept | Q2, Q9, Q10 |
| N:REQ-005-021 | finding | REQ-005-021 says 48 hours; SET-slot-hold-duration default 72; prd:140 | Q1: rule and setting default disagree; F1 |
| N:SET-acceptance-terms-text | cannot verify | | Default text is not in the PRD or the graph |

## Findings
1. F1 (N:REQ-005-021, Q1): what was compared, what is wrong, which side the sources support.

## Scenarios

### Scenario FLW-<id>
Main path, then each branch once (branch label in the Note column).

| Step | Actor | Screen | Reads | Writes | Rules | Events | Next stage | Note |
|---|---|---|---|---|---|---|---|---|
| STP-005-001 | ACT-patient | SCR-005-01 | ENT-subquote.price | | REQ-005-021 | | STG-main-03-accept | prd:86 |

### Scenario <short name>
(cancel or exit from a stage, timeout or expiry, money movement, actor outside its role, PRD edge case)

## Not checked or could not verify
<what was not checked and why; "None" must be followed by a sentence saying why>

Status: DONE | DONE_WITH_CONCERNS | BLOCKED | NEEDS_CONTEXT
Summary: ...
```

Rules for the report:
- **Verdicts table (gate).** Section heading exactly `## Verdicts`; one table with the columns Item, Verdict, Evidence, Note; one row per manifest item, item id copied exactly from the manifest; no other rows. Verdict is `OK`, `finding` or `cannot verify`.
- **Evidence (gate).** States what was compared with what. Graph ids are written bare (`REQ-005-021`, `ENT-quote.total`), with nothing attached to them. PRD lines are written `prd:N` or `prd:N-M` and refer to the review copy. An `OK` or `finding` row cites at least two different references (ids or PRD lines); fewer counts as a missing row (**Open for approval:** the threshold of two). A `cannot verify` row gives its reason in Note and is listed again under "Not checked or could not verify".
- **Findings found during a scenario** are recorded on the verdict row of the manifest item they concern, and referenced from the scenario's Note column. A step the graph cannot support is a finding.
- **Scenarios (gate for the FLW headings).** One `### Scenario <FLW-id>` per Flow in the manifest, walking its `next` links from the start step, every branch once, plus the main path. Then one `### Scenario <short name>` for: every cancel or exit path from each stage; each timeout or expiry; each money movement; each actor attempting something outside its role; each PRD edge case. Every step records actor, screen, fields read and written, rules applied, events emitted, next stage.
- **Citations (gate).** Every id in the Evidence column and in the Scenarios section exists in the review copy; every PRD line is inside the copy. Notes and the Findings list are not checked.
- **Not checked or could not verify (gate).** Always present. "None" alone is void.

## Report format (reviewer B)
Path: `plans/reports/tester-YYMMDD-frNNN-logic-review-adversarial-rN.md`.

```
# FR-NNN logic review, round N, reviewer B (adversarial)

Checklist: project-requirements/graph/checklists/logic-review.md v0.1
Reviewed: <A's report path>

## Attacks
| Item | A's verdict | B's verdict | Evidence | Note |
|---|---|---|---|---|
(one row per high-risk OK row of A; B's verdict is upheld or finding)

## New scenarios
### Scenario <short name>
(at least two A did not run, same table as A)

## Findings
(each is a miss by A)

## Rejections reviewed
(for each finding the controller proposes to reject: agree or disagree, with evidence)

## Not checked or could not verify
```
B's report has no gate in this draft (**Open for approval**).

## Sealed planted-defect file (controller only)
JSON, one per round (**Open for approval:** format and matching rule):

```
{"fr": "FR-005", "round": 1, "defects": [
  {"id": "D1", "kind": "reversed word", "items": ["N:REQ-005-021", "S:business-rules/general-module-rules"],
   "where": "copy/prd.md line 140, copy graph REQ-005-021 statement", "description": "after changed to before"}
]}
```
- `kind` is one of the five kinds in step 1; `items` are manifest item ids (the gate refuses ids not in the manifest).
- A defect counts as found when reviewer A's report has a `finding` row on at least one of its `items`. The controller lists every item a reader could reasonably attach the defect to, and no others.

## Gate checks (`scripts/logic_gate.py`)
The report is void when any holds:
1. A manifest item has no row; a row names an item not in the manifest, or a second row for an item.
2. A verdict is not `OK`, `finding` or `cannot verify`.
3. An `OK` or `finding` row cites fewer than two references; a `cannot verify` row gives no reason.
4. An id cited in Evidence or Scenarios is not in the review copy, or a cited PRD line is outside it.
5. A manifest Flow has no `### Scenario <FLW-id>` walkthrough (**Open for approval:** not in the phase file's step 4 list; added so a report cannot skip the walkthroughs).
6. The "Not checked or could not verify" section is missing, empty, or a bare "none".
7. A planted defect has no `finding` row on any of its items.

Before checking, the gate confirms the review copy still matches the manifest (sha256 of DB and PRD); a mismatch is bad input (exit 2), not a verdict.

## Exit rule per FR
All of the following in one round:
- Reviews A and B both complete, with zero new findings.
- The gate passed, including every planted defect found.
- Every fix from the previous round verified in place.

The user then reads the FR's final report; the FR is done only after that reading. If three rounds in a row still produce new findings, stop and report to the user: the FR likely has a structural problem that more rounds will not fix. The repeat rule in step 6 applies to single items earlier.

## Final report per FR
Path: `plans/reports/tester-YYMMDD-frNNN-logic-review-final.md`, kept by the controller across rounds:
- Findings ledger, one row per finding with columns: Finding, Round, Item, Question, Raised by (A or B), Outcome, Closed by (change-set, user decision, or rejection agreed by B), Verified in round.
- Per round: findings, voided reviews, planted-defect recall, misses B caught.
- Scenarios run (A and B), and what could not be verified.

## Reporting rules (controller)
- Status reports give counts of findings, rounds and voided reviews, planted-defect recall, and the misses B caught; never a pass rate on its own.
- A round with no findings is reported with its planted-defect recall as the evidence it was a real review.
- Any defect found after Phase 10 is logged as an escape in `plans/reports/logic-review-escapes.md`, one row per escape with columns: Date, FR, Defect, Found by, Question that should have caught it, Checklist change, New version. That question is fixed and this checklist's version goes up.

## Pass condition
For a round: the gate exits 0 on A's report, B's report is complete, and every finding has an outcome in the ledger. For an FR: the exit rule above, and the user has read the final report.

## Stop and ask when
- The repeat rule or the three-round rule triggers.
- A finding needs a business reading (two plausible rules): unclear item to the user, no fix.
- A proposed rejection has no agreement from reviewer B.
- The gate exits 2 twice for the same round (the copy or manifest is broken).
- A fix would change a node another FR owns or cites: the neighbour's boundary items reopen; tell the user before applying.

## Open for approval
1. Order of steps 1 and 2: the manifest is built on the planted copy (the phase file lists it first).
2. PRD under review: frozen baseline (the script default, as briefed) or the live compressed PRD after Phase 9.
3. Graph defects planted by direct SQL so the copy's change history does not reveal them; prefer defects `lint.py` does not report.
4. Evidence threshold: at least two distinct references for `OK` and `finding`.
5. Sealed file format and matching rule: a `finding` row on any listed item.
6. Gate check 5 (a walkthrough heading per manifest Flow) added beyond the phase file's step 4 list.
7. Reviewer B attacks every OK row on boundary edges, neighbour FRs, Flows, Steps, Stages, Actors, Settings and all Rules; B's report has no gate.
8. Unknown and repeated verdict rows void the report.
9. Reviewers may see the five defect kinds by reading this checklist.

## Change log
- 0.1 (2026-11-10): first draft from the phase 10 procedure (D39) under D43 item 6; not approved.
