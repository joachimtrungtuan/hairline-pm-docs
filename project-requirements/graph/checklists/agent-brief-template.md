# Agent brief template

Version: 1.1 (2026-11-08)

## Purpose
Every subagent in the programme receives a brief in this shape. The brief points at files and a checklist; it does not restate the rules. A brief that fits this template is enough for a fresh agent to do the task after the controller's context has been compacted.

## Constraints on the controller (standing rule 6, D18)
- Specific agent type (docs-manager, code-reviewer, tester, fullstack-developer); never general-purpose.
- At most 3 subagents running at once. Model Opus or lower; thinking High or lower. Cheap headless models only after the Phase 7 trial passes.
- Pass the working directory, timezone (Asia/Saigon) and language (English) in every brief. Every path in the brief is absolute or starts at the project root given as working directory; state line counts only after measuring them (`wc -l`).
- One agent owns one set of files; two agents never edit the same file, the DB, or the same change-set.
- The controller applies change-sets, runs backups, and holds every user approval. Subagents never run `write.py` against `graph.db`.

## Template

```
Task: <one sentence: the outcome, not the activity>
Programme: plans/261108-1040-requirements-graph-programme/plan.md — Phase <N>, <phase file>
Working directory: /Users/joachimtrungtuan/My Documents/Vân Tay Media/Products/Hairline (timezone Asia/Saigon, English, today <YYYY-MM-DD>)

Checklist to follow: project-requirements/graph/checklists/<file>.md v<X.Y>
  Re-read it in full before starting and again after any compaction. Your report must open with this path and version.
Also read: checklists/source-priority.md v<X.Y> (when the task touches sources)

Files to read (exact paths):
  - <frozen PRD path>
  - <graph files: schema.yaml, graph.json, README.md as needed>
  - <earlier reports that show the expected shape>

Files you may create or modify (nothing else):
  - <change-set path>  (create)
  - <report path>      (create)

Files you must not touch:
  - graph.db (the controller applies change-sets), main/, project-automation/, archived/, any live prd.md or CR file

Facts already verified by the controller: <counts, ids, states the agent would otherwise re-derive>

Decisions already made that constrain this task: <D-numbers or plan answers; one line each>

Acceptance criteria:
  - <pass condition items from the checklist, or a pointer to its "Pass condition" section>
  - Report at <plans/reports/{type}-{yymmdd}-{slug}.md> with every section the checklist names

Scope flags: <none | --yagni | --no-test ...> (state "none" explicitly)

Stop and ask when: see the checklist section of that name; write the question into the report and end with NEEDS_CONTEXT or DONE_WITH_CONCERNS instead of guessing.

End the report with:
Status: DONE | DONE_WITH_CONCERNS | BLOCKED | NEEDS_CONTEXT
Summary: one or two sentences
Concerns/Blockers: optional
```

## Report path convention
`plans/reports/{agent-type}-{yymmdd}-{slug}.md`, for example `plans/reports/docs-manager-261112-fr003-migration.md` and `plans/reports/tester-261112-fr003-completeness.md`. Reruns replace the file and state the previous counts in one line.

## Handling the status line
- `DONE`: controller verifies the acceptance criteria itself (count plus key fields plus one sampled section; never re-read a generated artifact whole).
- `DONE_WITH_CONCERNS`: controller moves every concern into the decisions note's "Still to decide" or the phase file before the next batch.
- `BLOCKED` or `NEEDS_CONTEXT`: change the context, scope or approach. Do not resend the same brief.

## Pass condition (for the brief itself)
Before sending, the controller checks the brief names: the checklist path and version, every file to read, the exact files the agent may write, the report path, the status line format, the scope flags, and the working directory and timezone.

## Change log
- 1.0 (2026-11-08): first version, from the orchestration protocol and D18.
- 1.1 (2026-11-08): paths absolute or root-relative, counts measured, after the FR-005 dry run reported a wrong report path and line count in its brief.
