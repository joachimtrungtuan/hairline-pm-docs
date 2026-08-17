# Four Service Routes Deck Revision

**Date**: 2026-08-17
**Update Type**: Major report revision (presentation deck)
**Status**: Revised, pending stakeholder review

## Summary

Revised the standalone presentation deck at
`local-docs/reports/2026-08-17/hairline-four-service-routes-deck/index.html`
from 12 slides to 23, after a cold-reader review found the deck understandable
to people who already know the platform but not to a first-time reader or to a
designer who has to draw the new flows.

The deck now runs as three named route sections framed by a human problem
statement, a shared vocabulary, and a closing design brief.

## Presentation Fixes

- **Windowed and fullscreen scaling**: the 1920x1080 stage is now absolutely
  positioned and centred on its own anchor (`translate(-50%, -50%) scale(s)`),
  recalculated on resize, orientation change, fullscreen change, and via a
  `ResizeObserver`. Previously the stage was a grid item and drifted right when
  scaled down in a window.
- **Font weights**: collapsed a 750/800/820/850/900 mix onto a 500/600/700
  scale. Headings and card titles are bold (700); body copy is 500; badge
  numerals are 700. Nothing renders at black weight.
- **Animation**: travel animations are expressed in percentages of their own
  track rather than hardcoded pixel distances; connectors carry a flowing
  gradient on a single per-slide tempo; the cross-platform loop is one packet
  relayed around four path segments on a 7.2s cycle; the hair-loss return path
  was re-drawn so it lands on the patient node instead of behind the conversion
  card.
- **Chrome**: removed the always-visible keyboard-hint label; the control bar
  now fades after 2.6s of idle and returns on any input.

## New Content

| Slide | Scene id | Purpose |
|---|---|---|
| 2 | `patient-problems` | Three patients the app cannot serve today, in their own words |
| 3 | `vocabulary` | Nine terms in plain language plus the case-state rail |
| 6 | `route-02-divider` | Section pause naming route 02 and its four slides |
| 8 | `hair-loss-story` | One patient across three months, patient action paired with system action |
| 11 | `route-03-divider` | Section pause naming route 03 and its four slides |
| 13 | `transplant-story` | The same narrative with the provider removed |
| 16 | `route-04-divider` | Section pause naming route 04 and its three slides |
| 18 | `aftercare-story` | Four gates: buy, assign, activate, run |
| 20 | `screens-inventory` | 39 screens across three platforms, counted from the FR screen specs |
| 21 | `edge-cases` | Six unhappy paths framed as states a designer must draw |
| 23 | `deck-recap` | Six takeaways covering the whole deck, plus the scope and open-decision counts |

Three swimlane "how the actors work together" slides for routes 02, 03 and 04
were added in the same revision, each with a data-input strip naming what
enters the flow at every phase.

## Review Passes After the Expansion

- **Route section dividers**: three full-bleed dark slides now separate the
  route sections (before routes 02, 03 and 04) so each section starts on a
  pause rather than mid-flow.
- **Card alignment**: the story timelines and the handoff and aftercare card
  rows use CSS subgrid and full-height cards, so every column shares the same
  baselines across the row and down the column.
- **Story milestones**: the patient timelines were relabelled from calendar
  dates (`Day 0`, `Day 1-14`, `Week 6`, `Month 3`) to the case phases that
  actually gate each step (`At creation`, `From the first log`, `Once
  assigned`, `Every advice cycle`, `Whenever he decides`). Neither FR-037 nor
  FR-038 defines a fixed schedule, so the dates asserted precision the
  requirements do not carry.
- **Handoff slide, redrawn**: the two-panel layout (four step cards beside a
  prose panel) was replaced by a single diagram of two case lanes joined by a
  payload bridge. The FR-038 lane carries the four beats and visibly continues
  past the exit point; the bridge names the five fields that actually cross,
  each tagged editable, swappable, replaceable or generated; a blocked line
  names what does not cross (price, payment, provider assignment, activation);
  the FR-011 lane below opens as a distinct record over its four gates; and a
  dashed fallback row states that an abandoned or failed conversion leaves the
  monitoring case active. Field names and their editability come from FR-038
  Screen 6 and the Integration Points list, not from the previous summary
  wording.
- **Aftercare path**: the eyebrow row is height-normalised so pill and plain
  labels put every card title on one baseline; the step numerals now carry a
  ring that only expands outward, replacing the scale-up-and-back pulse.
- **Closing slide**: the design ask was replaced by a recap of the whole deck -
  six takeaways plus a strip carrying 39 screens, 3 routes on one monitoring
  pattern, 6 unhappy paths, and 4 open product decisions. The four open
  questions remain recorded below and in the presenter notes.

## Source Traceability

- Route 02 content: `functional-requirements/fr037-monitor-hair-loss/prd.md`
  (Business Workflows, Screen Specifications, Business Rules)
- Route 03 content: `functional-requirements/fr038-monitor-transplant-progress/prd.md`
  (Main Flow, Alternative Flows A1-A3 and B1-B2, Screen Specifications).
  The handoff payload on slide 15 is taken from Screen 6 (field table and
  business rules) and Integration Points.
- Route 04 content: `functional-requirements/fr011-aftercare-recovery-management/prd.md`
  (Workflows 1, 2, 2b, 3, 4 and Screen Specifications)
- Screen counts are taken directly from the Screen Specifications headings of
  each PRD: patient 7/7/7, provider 3/0/5, admin 2/2/6.

## Open Questions Carried by the Deck

Counted on the closing recap and spelled out in the presenter notes:

1. How much should a patient know about provider response cadence before a
   provider is assigned?
2. Is the FR-011 scan-upload flow reused as-is for monitoring, or redesigned?
3. Does the patient see only the latest advice, or the full record across a case?
4. Does a completed case stay browsable in the app, or survive only as the
   exported PDF?

These are unresolved product decisions, not documentation gaps. They need an
owner before design work starts.
