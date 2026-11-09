# Checklist: source priority and unclear items

Version: 1.0 (2026-11-08)

## Purpose
Spell out standing rule 4 of the programme plan and decision D29 so every agent reads conflicting evidence the same way, and write unclear points in a form the user can decide on without reopening the files.

## Inputs
- `project-requirements/sources/source-register.md` (SRC ids, dates, lifecycle) and the meeting notes and briefs it links.
- Source nodes in the graph (`query.py cites <SRC-id>` shows what already relies on a source).
- The PRD line and any CR Decision evidence that names a source.

## Outputs
- `decided by` edges to the correct Source node.
- "Needs user decision" items in the migration or completeness report, in the format below.

## Trust order (D29, hybrid)
Read sources in this order and let the higher one win when they disagree:

1. **Raw transcript** (Source kind `transcript`) when one exists. For meetings 1 to 3 none persists, so skip this level for `SRC-MTG-001`, `SRC-MTG-002`, `SRC-MTG-003`.
2. **Cleaned meeting notes** (`meeting-notes`): the `SRC-MTG-00N` notes in `sources/meetings/`. For meetings 1 to 3 these are the originals and are relied on alone.
3. **Later meetings and stakeholder documents override earlier ones.** A later dated source wins over an earlier one on the same topic. The fund release brief `SRC-DOC-001` (2026-09-08) is a stakeholder document and sits in this layer by its date.
4. **Product owner decision logs** (`project-requirements/reports/.../mtg002-quote-model-decisions-2026-10-16.md` and similar) record how the PO refined a meeting item. They rank above the PRD and below the stakeholder source they refine. They are becoming Source nodes (carried item, D28); until then cite the stakeholder item they refine and name the log in the note.
5. **PRD text** is the weakest. It is the thing being checked, not the evidence.
6. **Change Requests are never sources** (D14). Use a CR only to find the source its Decision evidence names.

Rules cite the notes by default. Cite a transcript line only when the notes and transcript differ or the notes are ambiguous.

## Examples
- The PRD says the slot hold lasts 72 hours; `SRC-MTG-002-D05` says 48 hours; nothing later changes it. The source wins: node default 48, PRD line listed as `partial` in the completeness check, no decision needed, note "PRD line NNN out of date against SRC-MTG-002-D05".
- `SRC-MTG-002` (2026-09-09) says quotes expire after 14 days; `SRC-MTG-003` (2026-09-17) says expiry is configurable by admin. Later wins: a Setting owned by FR-026, default 14, governed-by edge; cite both sources.
- The PRD line 561 says admin cancellation writes a supersession record; five other PRD lines and the Key Entities say it does not; no source covers it. Sources are silent and the PRD contradicts itself: write an unclear item (format below). The graph follows the majority reading and says so.
- A rule has no meeting item at all. Leave it without `decided by`; lint L10 records the gap; do not invent a source and do not attach the nearest topic.
- The CR for FR-011 lists "assignee history" with Decision evidence `SRC-MTG-002-D11`. The edge goes to `SRC-MTG-002-D11`, not to the CR.

## Unclear item format
Write every conflict or gap as one numbered item the user can answer in a sentence:

```
N. <Topic in five words or fewer>
   What the PRD says: "<quoted line>" (prd.md line NNN)
   What the source says: "<quoted item>" (SRC-..., date) — or: no source covers this
   Why it matters: <one sentence: which rule, field or screen changes depending on the answer>
   What the graph holds now: <node id and the reading applied, or "nothing yet">
   Options: (a) ... (b) ... (c) something else
```

Plain words. No model jargon in the first line; the user should understand the question without opening the PRD. One item per conflict; do not bundle.

## Pass condition
- Every `decided by` edge points at a stakeholder or transcript Source, never a CR or a PRD.
- Every disagreement between sources, or between a source and the PRD, that the agent noticed appears as an unclear item or as a one-line "later source wins" note with both ids.
- No agent-chosen override: where two readings remain plausible, the item is open and the graph records which reading was applied provisionally.

## Stop and ask when
- Two sources of the same layer and date disagree.
- A later source appears to reverse a decision the user has already recorded in the decisions note (D1 to D30 or a Phase 4 decision).
- A source the PRD cites is not in the register.
- Applying the trust order would retire or change a node another FR already cites (`query.py cites` non-empty): write the item up and leave the node as is.

## Change log
- 1.0 (2026-11-08): first version from standing rule 4 and D29; PO decision logs placed between stakeholder sources and PRD text pending their Source nodes (D28 carried item).
