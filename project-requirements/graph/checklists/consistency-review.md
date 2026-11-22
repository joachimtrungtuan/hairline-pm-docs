# Consistency review (boundaries and flow between FRs)

Version: 1.0 (2026-11-22)

Used by Phase 8 of the requirements graph programme. The checks are queries, not reading: `scripts/query.py boundary`, `ownership`, `flow`, `joins`, `coverage` (code in `scripts/consistency.py`). A row is a finding for a person to judge. The queries cannot tell data that two FRs share on purpose from data one FR took by mistake.

## What each finding means and how it is settled

| Command | Finding | Meaning | Settled by |
|---|---|---|---|
| boundary | screen shows field | A Screen of one FR shows Fields of an Entity another FR owns, and the first FR has no `references` link to any Rule of the owner | See "Boundary verdicts" |
| boundary | rule applies to data | A Rule of one FR applies to an Entity or Field another FR owns, with no `references` link | See "Boundary verdicts" |
| ownership | same name or same table, different owners | Two FRs each own a node that looks like the same thing | Keep one owner; the other FR links to it. A real difference in meaning: rename one |
| ownership | field owner differs from entity owner | A Field is owned by another FR than its Entity | See "Ownership verdicts" |
| flow | event emitted, no rule applies to it | Nothing in the graph reacts to the Event | Find the PRD line that uses the Event (often a notification in FR-030) and link its Rule; if no PRD uses it, ask |
| flow | entity written, never read | Data is stored and no Stage uses it | Find the PRD line that reads it and add the Stage link; if none, ask whether the data is needed |
| flow | entity read, never written | A Stage uses data no Stage creates | Usually configuration an admin maintains: add the write at the Stage of the admin Screen; if no Screen maintains it, ask |
| flow | entity read only before it is written | On one timeline the only readers come before the only writers | Check the PRD order; a real order conflict is an owner decision |
| flow | stage reads no data | A Stage has no incoming data | An empty Stage (no writes, events or Rules) is a filing note; one with Rules needs its reads added from the PRD |
| joins | read at entry, not written upstream | A Stage entered from another timeline reads data that neither timeline has written by then | Data kept on an account timeline (patient, provider, configuration) is accepted; anything else is checked in the PRD |
| joins | join carries no data the joined stage reads | A timeline joins another and hands nothing over | Add the read from the PRD or ask |
| coverage | screen without actor, stage without actor, rule without stage | A link is missing | Add it from the PRD |

## Boundary verdicts (exactly one for each FR pair)

- `intended`: the first FR's PRD names the owner FR as a dependency, or the Screen plainly displays the owner's data read-only. Fix: add a `references` link from the first FR to the owner's Rule that defines that data. No owner question.
- `misfiled`: the Rule or Field really belongs to the other FR (the PRD of the first FR does not state it, or states it only by pointing at the owner). Fix: move or merge it in a change-set.
- `conflict`: both PRDs state a rule for the same data and the two differ (a limit, a default, who may change it, a status list). This is an owner decision. Quote both lines.
- `unclear`: the PRDs do not say who owns the data. Owner decision, with a recommendation.

## Ownership verdicts

A Field belongs to the FR that owns its Entity unless the PRD of the other FR is the only one that defines it. Then either the Field moves to an Entity that FR owns, or the owner FR's PRD gains the line. Decide by which PRD states the Field's meaning; ask only when both do and they differ.

## Flow alignment (one report for each FR)

Follow `prd-structure.md`, section "Flow alignment check": compare each Business Workflows flow of the PRD with the graph's Stage sequence and cross-FR links. In the same pass, close the FR's open hand-offs (lint L18): a Step with `handoff_to` or `handoff_from` is stitched with a `next` link to the matching Step of the other FR, or the hand-off is reported as having no matching Step.

## Decision requests

Only a `conflict`, an `unclear` owner, or data nobody uses goes to the owner. Each request is written so a non-technical owner can answer without opening a file: what the feature is, what each PRD says (quoted, with FR and line), the options, a recommendation and why. No ids without an explanation. Filing choices are made by the reviewer and recorded.

## Pass condition

Every finding row has one verdict and either a change-set operation, a recorded acceptance with its reason, or a decision request. The five commands are re-run after the change-sets; rows that remain are the accepted ones and are listed in the phase report.

## Stop and ask when

- Two PRDs give different values for the same thing.
- A fix would remove a requirement that a PRD states.
- A hand-off names an FR whose PRD has no receiving step.

## Change log

- 1.0 (2026-11-22): first version, written with the five query commands.
