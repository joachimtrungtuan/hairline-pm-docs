# Meeting 03 Source Extraction — 2026-09-18

## Summary

Recorded the 17 September 2026 stakeholder meeting as source `SRC-MTG-003` and registered it in the subsequent stakeholder source register. No PRD, Change Request, schema, design, or roadmap document was modified.

## Files Changed

| File | Change |
|---|---|
| `sources/meetings/meeting-03-quote-flow-feedback-localization-and-website.md` | Created |
| `sources/source-register.md` | Added the `SRC-MTG-003` row; extended missing provenance and incorporation status |

## Scope Decision

The meeting opened with a project-team walkthrough of the three-level quote hierarchy (parent quote → quote option → sub-quote). The Product Owner confirmed this was a status report on work already decided and incorporated through `CR-FR004-20260909-01`, `CR-FR005-20260915-01`, and `CR-FR006-20260915-01`, not a new stakeholder decision. It is therefore recorded under a `Reported Status` section as background only, and the extraction focuses on the stakeholder feedback and new direction.

## Items Recorded

- **D01–D04** — Quote flow: reduce seven steps to about five by grouping optional inputs; graft count stays a comparison signal, not a pricing input; surface the inquiry head-scan gallery inside the quote flow with annotation to a derived image set; no bulk or copy-paste quoting, to preserve review friction against the medical-alert flags.
- **D05–D07** — Localization: Turkish first via an imported JSON translation package; readers are served their own preferred language; free text between parties (patient concern, notes, messages) is machine-translated into the reader's base language, scoped to defined fields and controllable per reader.
- **D08–D09** — Website: collapse the hamburger menu into accordion sections, remove non-destination category headers, keep unpublished page templates restorable; replace placeholder feature imagery and avoid overpromising wording.
- **D10–D11** — Billing: redesign Admin billing to reflect the two payout rails; automate the manual rail through the banking provider's API with an automatic release window.
- **F01** — Deferred: assisted or automatic quoting tied to external clinic-availability integration.
- **P01–P03, O01–O05** — Operational follow-ups and five open questions, including the still-unset 48/72-hour confirmation window, which repeats `MTG-002-D08` and `MTG-002-O02`.

## Status and Next Steps

`SRC-MTG-003` is **pending review**. Nothing in it authorizes implementation. The quote-flow items (D01, D03) and the localization and billing items require Change Requests against their owning contracts before any build, and D10/D11 should be reconciled together with the pending payments brief `SRC-DOC-001`.

Participant names and roles, and the clinic-diary and banking providers named phonetically in the transcript, are flagged for confirmation.

## Post-Creation Corrections (2026-09-18)

- Product Owner confirmed **Underpin Health** (external clinic system) and **Revolut** (banking provider); both are now stated as fact rather than transcript approximations, and the confirmation item was removed from `Validation Needed`.
- Product Owner clarified that **five steps is a design target, not an acceptance criterion** for the quote flow. `MTG-003-D01`, `MTG-003-O01`, and the requirement-routing row were reworded so the binding requirement is a materially shorter flow, with the final step count following from the grouping design.
