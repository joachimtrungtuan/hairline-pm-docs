# Checklist: PRD structure audit

Version: 1.0 (2026-11-09)

## Purpose
Record, for one frozen FR PRD, what each section contains, how long it is, and whether the same content exists elsewhere, so that the programme can decide (Phase 6, user approval) what a rendered PRD keeps, omits, or de-duplicates. The audit is read-only and makes no recommendation about what to cut; it only classifies and measures.

## Inputs
- The frozen PRD: `archived/prd-baseline-2026-11-08/frNNN-slug/prd.md` (project root; read-only).
- `graph/schema.yaml` (node types only, to name the graph home of a content class).
- Nothing else. Do not read the live PRD, Change Requests, migration reports, or other audit reports.

## Reading rule
List headings with `rg -n "^#{1,4} " <prd>`. Read every section, but only by line range from that heading list, at most 250 lines per read. Never read a whole file; three PRDs exceed 1800 lines.

## Outputs
One report per FR at the path given in the brief, in the format below. A report has one table row per heading (levels 2 to 4), plus a totals block.

## Content classes
Use exactly one primary class per heading. Add a second class in brackets only when the section mixes two classes about evenly.

scope, actor, flow, screen, field, rule, user story, event, setting, success metric, dependency, assumption, technical note, CR history, open question, approval, glossary, repetition (the section restates another section), other (say what).

## Duplicate column
For each heading, state whether the content exists elsewhere, with the location:
- `none`: the content appears only here.
- `same PRD: <heading>`: the same facts appear under another heading of this PRD (for example rules restated under each screen, fields listed both in a screen table and in Key Entities).
- `other FR: FR-NNN <topic>`: the section describes behaviour that another FR's PRD owns (payments, notifications, messaging, settings). Name the FR from the PRD's own cross-references; do not open the other PRD.
- `graph`: the content class has a node type in `schema.yaml` (Rule, Entity, Field, Screen, Event, Setting, Actor, Stage, Source), so the graph already holds or will hold it.
Several values may apply; separate with `;`.

## Steps
1. Re-read this checklist. Write the header: checklist path and version, FR id, PRD path, total line count.
2. Produce the heading list. For each heading record: heading text with level, start line, end line (the line before the next heading of the same or higher level), line count.
3. Read each section by range and assign the content class, the duplicate value, and a note of at most 25 words naming anything unusual (rules hidden in technical notes, a flow that is really a screen list, a section that is empty or a placeholder).
4. Fill the totals block: lines per content class, lines whose duplicate value is `none`, lines marked `same PRD`, lines marked `other FR`, lines marked `repetition` class.
5. Do not recommend keeping or omitting anything. Do not fix the PRD.

## Report format

```
# FR-NNN PRD structure audit

Checklist: project-requirements/graph/checklists/prd-audit.md v1.0
PRD: archived/prd-baseline-2026-11-08/frNNN-slug/prd.md (N lines)
Headings audited: N

| # | Heading (level) | Lines | Count | Class | Duplicate | Note |
|---|---|---|---|---|---|---|
| 1 | ## 1. Executive Summary (2) | 12-30 | 19 | scope | none | |
...

## Totals
| Class | Lines | Share |
|---|---|---|
...
Lines with duplicate = none: N
Lines marked same PRD: N
Lines marked other FR: N
Lines of class repetition: N

## Unusual findings
- ...

Status: DONE | DONE_WITH_CONCERNS | BLOCKED
Summary: one sentence
```

## Pass condition
Every heading of level 2 to 4 has a row; line counts sum to the PRD total (allowing for front matter before the first heading, reported as one `front matter` row); each row has a class and a duplicate value; no recommendation appears.
