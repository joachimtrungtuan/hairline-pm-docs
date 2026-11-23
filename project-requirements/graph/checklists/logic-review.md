# Checklist: FR logic review

Version: 1.0 (2026-11-23), set by the owner's gate 2 ruling after the FR-005 pilot

The pilot (two rounds on FR-005, report `plans/reports/pm-261123-1120-fr005-logic-review-pilot.md` at the project root) showed the v0.2 procedure finds real defects but does not converge and costs too much to repeat on 37 FRs. The owner ruled on 2026-11-23: two passes per FR, no third pass, and the aim is not an error-free result. The section "Procedure v1.0" below is the procedure in force. The sections after it that describe Reviewer A's verdict table, Reviewer B, the sealed planted-defect file, the gate and the v0.2 exit rule are kept as the record of the pilot and are not run. "Logic classes and their questions" and "Checks reused from other checklists" still apply.

## Procedure v1.0 (in force)

Two passes per FR, then the FR is closed. One agent at a time; every agent is a fresh Sonnet agent with no history.

**Inputs for a reviewer**: this section and "Logic classes and their questions"; the FR's live PRD; the FR's manifest in Markdown with the flow paths of other FRs removed (`scripts/logic_manifest.py FR-NNN --format md`, then keep only `### Path of FLW-NNN-…` sections of the FR under review); the graph, read-only (`scripts/query.py`, `sqlite3 -readonly`); `graph/schema.yaml`; neighbour PRDs by section, only at a hand-off point. A reviewer writes nothing but its report.

1. **Pass 1, review.** One adversarial reviewer looks for logic defects in what the FR owns: its rules, steps, flows, screens, fields, states and its hand-offs to and from neighbours. It reports findings only, each with the item id, the evidence (PRD line or graph row) and a proposed fix. No verdict row per item. It ends with a short list of what it did not check.
2. **Triage (controller).** Each finding becomes: fix; owner decision (a real business choice only); rejected (with the evidence); or neighbour (the defect sits in another FR's item). Neighbour findings go to the shared ledger and are not fixed here.
3. **Pass 1, fix.** One fixer writes the change-set and the PRD edit. The controller checks the change-set, backs up `graph.db`, applies it with `write.py`, reruns lint, exports, commits.
4. **Pass 2, review.** A different fresh reviewer gets the list of pass 1 fixes, confirms each one holds, and looks once more for defects, with attention to what the fixes added or changed. Same report form.
5. **Pass 2, fix.** As step 3. Findings that are not worth a graph change go to the implementation backlog with a reason.
6. **Close.** The FR's ledger rows are final. There is no third pass. A pass 2 finding that needs the owner is asked once; the FR closes without waiting if the answer is not needed for other FRs.

**After all FRs**: one cross-FR pass settles the neighbour rows of the shared ledger (`plans/reports/logic-review-ledger.md`), grouped by the FR that owns the item.

**Planted defects**: not used per round. The controller may plant defects in a copy as a spot check of reviewer attention on a sample of FRs.

**Pass condition per FR**: both passes ran, every finding has a ledger outcome, every accepted fix is applied and lint is not worse than before the FR started.

**Stop and ask the owner** only for a real business decision, or when a fix would change an owner ruling.

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
1. **Review copy and planted defects (controller).** Make a fresh round folder in the session scratchpad: `logic-review/FR-NNN/rN/copy/` holding a copy of `graph.db` and of the live compressed PRD (`functional-requirements/<module>/prd.md`, which the manifest script defaults to), never the frozen baseline under `archived/`, so a fix made in one round is in front of the next round's reviewer. Plant 3 to 5 defects, drawn in rotation from the kinds below, at least one a one-word change, all different from earlier rounds:
   - contradicting threshold across FRs;
   - reversed word (before/after, minimum/maximum, may/must);
   - removed link;
   - unreachable stage;
   - actor permission swap.
   Graph defects are made with direct SQL on the copy, not with `write.py`, so the copy's change history does not show them. Prefer defects that `lint.py --db <copy>` does not report. Record each defect in the sealed file (format below) in `logic-review-sealed/FR-NNN-rN.json`, a scratchpad folder outside the round folder. The real graph and PRDs are never touched.
2. **Manifest (script).** Build it on the copy, after planting (built from the unplanted graph, a removed link would still be a manifest row and give the defect away):
   ```
   /usr/bin/python3 scripts/logic_manifest.py FR-NNN --db <round>/copy/graph.db --prd <round>/copy/prd.md --out <round>/manifest.json
   /usr/bin/python3 scripts/logic_manifest.py FR-NNN --db <round>/copy/graph.db --prd <round>/copy/prd.md --format md --out <round>/manifest.md
   ```
   Without `--prd` the script reads the live compressed PRD of the FR's `module`; the commands pass the copy explicitly. The manifest lists every item; the reviewer does not choose what to look at. Its item ids are stable across rounds, so the ledger can count findings per item (repeat rule).
3. **Review A.** Brief per `agent-brief-template.md`, pointing at this checklist and the inputs above. The reviewer writes the report in the format below: a verdict row for every manifest item, the scenario walkthroughs, the findings list, and the "Not checked or could not verify" section.
4. **Gate (script).**
   ```
   /usr/bin/python3 scripts/logic_gate.py --manifest <round>/manifest.json --report <report> --defects <sealed file>
   ```
   Exit 0 pass, 1 void, 2 bad input. A void report is never patched: a new reviewer A reruns the round on the same copy and manifest. Record the planted-defect recall the gate prints. The gate output is never shown to a reviewer.
5. **Review B (adversarial).** A different fresh agent receives A's report and the same copy. It attacks every OK verdict in A's report on the high-risk items (below) and runs at least two scenarios A did not. Anything B finds is recorded as a miss by A. The controller then runs the B coverage count (see "Gate checks"): how many of A's high-risk OK rows B's Attacks table names.
6. **Triage (controller with reviewer B and the user).** Each finding gets one outcome:
   - **fix**: goes to the fixer;
   - **user decision**: written in `source-priority.md` unclear-item format and sent to the user;
   - **rejected**: only with evidence plus agreement from reviewer B.
   Nothing is closed as minor or out of scope without the user. **Repeat rule:** when the same manifest item draws a finding for the third time, or the FR has findings in a third round, it stops and waits for the user's decision; no further fix or rejection on it until then.
7. **Fix.** The fixer writes a change-set and the matching PRD edit, each citing the finding (`FR-NNN rN F<n>`). The controller backs up `graph.db`, applies the change-set, then has the touched PRD lines re-checked under `completeness-check.md`.
8. **Next round.** Repeat from step 1 on the whole FR, not only the changed lines, with fresh reviewers and new planted defects.

## High-risk items for reviewer B
B attacks every row A marked OK whose item is: a boundary edge, a neighbour FR, a Flow, a Step, a Stage, an Actor, a Setting, or a Rule. These carry the money, time, permission, status-change and boundary logic the phase file names; Rules cannot be sorted into those classes mechanically, so all are attacked; B does not select the rows itself, since that would let the reviewer choose what to look at.

## Report format (reviewer A)
Path: `plans/reports/tester-YYMMDD-frNNN-logic-review-rN.md`. The gate parses the parts marked (gate).

```
# FR-NNN logic review, round N, reviewer A

Checklist: project-requirements/graph/checklists/logic-review.md v0.2
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
- **Evidence (gate).** States what was compared with what. Graph ids are written bare (`REQ-005-021`, `ENT-quote.total`), with nothing attached to them. PRD lines are written `prd:N` or `prd:N-M` and refer to the review copy. An `OK` or `finding` row cites at least two different references (ids or PRD lines); fewer counts as a missing row. A `cannot verify` row gives its reason in Note and is listed again under "Not checked or could not verify".
- **Findings found during a scenario** are recorded on the verdict row of the manifest item they concern, and referenced from the scenario's Note column. A step the graph cannot support is a finding.
- **Scenarios (gate for the FLW headings).** One `### Scenario <FLW-id>` per Flow in the manifest, walking its `next` links from the start step, every branch once, plus the main path. Then one `### Scenario <short name>` for: every cancel or exit path from each stage; each timeout or expiry; each money movement; each actor attempting something outside its role; each PRD edge case. Every step records actor, screen, fields read and written, rules applied, events emitted, next stage.
- **Citations (gate).** Every id in the Evidence column and in the Scenarios section exists in the review copy; every PRD line is inside the copy. Notes and the Findings list are not checked.
- **Not checked or could not verify (gate).** Always present. "None" alone is void.

## Report format (reviewer B)
Path: `plans/reports/tester-YYMMDD-frNNN-logic-review-adversarial-rN.md`.

```
# FR-NNN logic review, round N, reviewer B (adversarial)

Checklist: project-requirements/graph/checklists/logic-review.md v0.2
Reviewed: <A's report path>

## Attacks
| Item | A's verdict | B's verdict | Evidence | Note |
|---|---|---|---|---|
(one row per high-risk OK row of A, with the manifest item id copied exactly into the Item column; B's verdict is upheld or finding)

## New scenarios
### Scenario <short name>
(at least two A did not run, same table as A)

## Findings
(each is a miss by A)

## Rejections reviewed
(for each finding the controller proposes to reject: agree or disagree, with evidence)

## Not checked or could not verify
```
B's report has no gate and is never voided. The controller counts coverage with `logic_gate.py --b-report` (see "Gate checks").

## Sealed planted-defect file (controller only)
JSON, one per round:

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
5. A manifest Flow has no `### Scenario <FLW-id>` walkthrough (not in the phase file's step 4 list; added so a report cannot skip the walkthroughs).
6. The "Not checked or could not verify" section is missing, empty, or a bare "none".
7. A planted defect has no `finding` row on any of its items.

Before checking, the gate confirms the review copy still matches the manifest (sha256 of DB and PRD); a mismatch is bad input (exit 2), not a verdict.

**Reviewer B coverage count** (controller only; not a gate on B and never a reason to void anything):
```
/usr/bin/python3 scripts/logic_gate.py --manifest <round>/manifest.json --report <A report> --b-report <B report>
```
It reports how many OK rows reviewer A gave on the high-risk items (previous section), how many of those the Item column of B's `## Attacks` table names by item id, and the list of those B did not name. It exits 0 whenever both reports and the manifest parse, and 2 when one does not (for example B's report has no `## Attacks` table). The controller sends the unnamed list back to B to attack; B stays free to argue any verdict.

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

## Settled 2026-11-23
The owner approved the procedure and this checklist for the FR-005 pilot on 2026-11-23 with the nine drafting choices and three questions below settled as shown (source: `plans/261108-1040-requirements-graph-programme/phase-10-completion-plan.md`). The owner can overrule any of them in the review after the pilot.

| # | Choice | Settled as | Reason |
|---|---|---|---|
| 1 | Manifest built on the planted copy | Yes | The reviewer and the gate must count the same items |
| 2 | Which PRD is copied for review | The live compressed PRD, never the frozen baseline | A fix made in round 1 must be in front of the round 2 reviewer; the baseline never receives fixes |
| 3 | Defects planted by direct SQL on the copy | Yes | The copy is throwaway; the real graph is still written only through `write.py` |
| 4 | Evidence threshold of two distinct references per OK verdict | Yes | One reference proves nothing was compared |
| 5 | Sealed defect file as JSON in the session scratchpad | Yes, and copied into `plans/reports/` after the round closes | The scratchpad can be cleared; the record of what was planted must outlive the round |
| 6 | One `### Scenario <FLW-id>` section per manifest Flow | Yes | Lets the gate count walkthroughs |
| 7 | Reviewer B attacks every OK row in the high-risk classes; no gate on B | Yes, plus one controller count: B's report must name each OK row it attacked | Keeps B free to argue, but proves B covered the rows |
| 8 | Unknown or repeated verdict rows void the report | Yes | A patched report is the failure this phase is built against |
| 9 | Reviewers may see the five defect kinds | Yes for the pilot; recall is measured, and kinds are added if every round scores full recall with no effort | The procedure already tells reviewers defects exist |

| Question | Answer |
|---|---|
| Which PRD the review reads | The live compressed PRD (same as choice 2) |
| What counts as an event consumer | A Rule that `applies to` the Event, or a PRD trigger line that names it |
| Nothing mechanical stops a reviewer reading the real files | Accepted. The brief gives only the review folder, and a reviewer who reads the real files misses the planted defects, which voids the report |

## Change log
- 0.1 (2026-11-10): first draft from the phase 10 procedure (D39) under D43 item 6; not approved.
- 0.2 (2026-11-23): approved by the owner for the FR-005 pilot. Nine drafting choices and three questions settled (section "Settled 2026-11-23", replacing "Open for approval"); the review reads the live compressed PRD instead of the frozen baseline; added the reviewer B coverage count to the gate checks; banner removed.
- 1.0 (2026-11-23): owner gate 2 after the FR-005 pilot. Two passes per FR with one adversarial reviewer per pass, findings-only reports, neighbour findings to a shared ledger, no per-round planted defects or gate, no third pass. The v0.2 sections stay as the pilot record.
