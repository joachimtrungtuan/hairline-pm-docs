---
source_id: SRC-MTG-003
source_type: stakeholder-meeting
meeting_date: 2026-09-17
captured_on: 2026-09-18
validation_status: pending-review
incorporation_status: not-incorporated
---

# Meeting 03: Quote Flow Feedback, Localization, and Website

## Context

The meeting had three parts: a project-team walkthrough of the revised quote structure and provider quoting flow, a review of website progress, and a first look at the Admin billing and localization areas.

The revised quote hierarchy was presented as a status report on work already decided and under implementation, not as a new decision for stakeholder approval. It is recorded here as background only (see "Reported Status"). The requirement value of this meeting is the stakeholder feedback and new direction captured in "Confirmed Decisions and Directions".

Participant names and roles require confirmation. Evidence was a rough transcript held outside the repository and not copied into the project.

## Reported Status

Background only. These statements describe what the project team reported as already decided or in progress; they are not new stakeholder decisions and do not authorize contract changes on their own.

- The quote data model was rewritten to three levels: a parent quote (one provider response, the unit counted for analytics), quote options (the packages offered), and sub-quotes (the date-range and price records under an option). The patient accepts a sub-quote, which inherits the parent quote's information.
- Cardinality as reported: one inquiry receives quotes from multiple providers; one provider may submit multiple quotes; one quote holds multiple options; one option holds multiple date-and-price records.
- The provider quote creation flow was reported as seven steps: treatment and package selection, estimated grafts and visual plan, treatment dates and appointment details, pricing, promotion codes, clinician and treatment plan, then notes and documents.
- Inline package customization saves to the quote only and does not write back to the provider catalog. Customized packages carry a visual cue distinguishing them from unmodified presets.
- Quote review and editing were consolidated into a single screen with tabbed detail sections.
- Backward compatibility with the existing mobile API schema was reported as preserved; the backend team was reported as already building the new schema, with frontend work outstanding.
- Admin has full visibility of accepted quote pricing, and Admin may correct information that is locked for the patient and provider at that stage.
- Provider billing and invoicing backend logic was reported as complete but untested and without seed data.
- All website pages were reported as built, with publication state controlled per page; supplied content has been applied.
- Automatic translation capability exists in the system but is deliberately not activated because of per-translation AI cost.

## Confirmed Decisions and Directions

### MTG-003-D01: Reduce the provider quote flow to about five steps

The seven-step quote flow is too long. It should be collapsed to approximately five steps.

Five steps is a design target to work toward, not an acceptance criterion. The binding requirement is a materially shorter flow; the final step count follows from the grouping design.

Optional and low-frequency inputs should be grouped rather than each occupying its own step. Estimated grafts, visual plan, notes, and attachments were named as candidates to combine into a single tab, because notes and attachments are not needed on every quote.

Stakeholders raised the overlap between "treatment and package" and "select treatment date", which appear as separate steps for related decisions.

Stakeholders did not accept coupling graft count to pricing as part of the simplification. See MTG-003-D02.

### MTG-003-D02: Graft count is a comparison signal, not a pricing input

A proposal to derive price from graft count was rejected as a general rule. Some clinics quote per graft, notably in markets such as the UK; others, notably in Turkey, quote irrespective of graft count.

Graft count remains valuable as a patient comparison signal, because patients compare what each provider commits to deliver at a given price. The system must not assume a per-graft pricing model.

Estimated grafts remain manually entered by the provider. They are not derived automatically from the patient's submitted media.

### MTG-003-D03: Surface patient head-scan images inside the quote flow

Providers currently cannot view the patient's head-scan images while building the quote; the images are only visible on the inquiry detail screen. Providers must therefore save images locally and annotate them externally to produce a visual plan, which stakeholders described as excessive work.

The head-scan gallery for the inquiry should be available inside the quote flow, with in-place annotation: the provider can open an image, draw, and highlight.

Annotations must be written to a separate derived image set. The patient's original head-scan images must remain unmodified.

An annotated image is not mandatory output; the requirement is provider convenience during assessment.

### MTG-003-D04: No bulk or copy-paste quote creation

A provider-requested ability to copy a previous quote and clear the patient identity was discussed and not adopted for now.

Two reasons were given. First, package presets already carry the reusable content, so the step-through flow exists mainly to vary what differs per patient: treatment dates, location, clinician, and treatment plan. Second, and treated as the stronger reason, quoting must retain enough friction that the provider actually reads the patient's details, especially medical history and the automatic medical-alert flags raised from inquiry answers. Bulk submission risks quoting a patient the provider cannot safely treat, or mispricing.

### MTG-003-D05: Localization, starting with Turkish

The system currently operates in English only. Admin already exposes a language list, and new languages are added by importing a translation package: a JSON file keyed one-to-one against the English text keys.

Turkish is the agreed first target language. Turkish uses a left-to-right Latin alphabet with diacritics, so no bidirectional layout work is implied. Further languages, German was named as an example for advertising markets, follow later.

The project team will export the full text-key list from the system and hand it to the stakeholder side, with guidance, for translation. The completed package is then imported and tested.

### MTG-003-D06: Language served follows the reader's preference

Patients select their language in the app and must read quotes and downstream pages in that language. English is the default, not a forced presentation language.

The stakeholder objective is accurate translation so that no confusion arises in quote and treatment content.

### MTG-003-D07: Free-text between parties must be machine-translated

Preset interface text is only part of the problem. Free-text written by either party, the patient's concern field first of all, provider notes, and messages, will cross language boundaries; an Arabic-language inquiry may reach a UK provider.

The agreed model is the one used by short-let marketplaces: translate incoming free text into the reader's own base language automatically, rather than requiring either party to translate manually.

Two constraints were attached. Translation should be limited to defined fields, and the per-field character limits already present in the forms bound the cost. Auto-translation should be controllable rather than always on: a reader who can read the source language should be able to leave it untranslated, via an explicit translate action or an on/off switch, with messaging threads named as the case for a persistent switch. The languages a provider declares in their profile can drive this default.

Cost was accepted as modest because only short strings are translated, not documents.

### MTG-003-D08: Website navigation should collapse, not expose everything

The full-width expanded menu panel is too cluttered. The hamburger menu should use collapsed accordion sections that expand on click, for example a "Patients" section revealing its child pages.

Category headers that are not destinations, such as the marketing and patients headers, should be removed as links. Core pages, such as the homepage, "How it works", "About", and content, belong directly in the bar; the deeper treatment and patient pages belong inside the collapsible menu.

Pages withheld from publication must keep their templates intact for later reuse. Section-level items are hidden in the page builder and page-level items are held in draft, so both remain restorable.

### MTG-003-D09: Replace the placeholder feature imagery

The feature images on the website do not demonstrate the feature. The scan progress timeline image conveys wording rather than a visible result, and the video follow-up image shows two full-hair subjects. Both should be reworked so the image shows the actual capability.

Wording must not overpromise beyond what the product delivers. The earlier "our AI overlay" phrasing was corrected to describe the app comparing head-scan versions across time; the project team holds editorial judgement here provided nothing is overstated.

### MTG-003-D10: Billing screens must reflect the two payout rails

The Admin billing and invoices area shows per-provider and per-patient invoices with the commission, net payout, payment status, and whether a manual action is required.

The screen predates the revised payment structure and needs redesign so that it presents the correct fields per payout rail, including payout date and expected payout date for the connected-account rail, and the manual confirmation action for the accountant-paid rail.

### MTG-003-D11: Automate the manual payout rail

The manual rail should not stay manual. The banking provider used, Revolut, exposes an API that can execute payouts programmatically.

The release trigger should mirror the connected-account rail: the patient has a fixed window, 48 or 72 hours as discussed without a final value, to confirm or raise a problem, and the payout releases automatically if no response arrives.

This item relates to the written payments brief (SRC-DOC-001), which the project team had received but not yet reviewed in detail at the time of the meeting.

## Future Direction

### MTG-003-F01: Assisted or automatic quoting

Automatic quoting was raised as a later improvement, not current scope: where defined criteria match, such as a clean medical history within a set age range, and where image assessment can confirm the case fits the provider's standard category, the system could offer the provider an auto-quote path.

Its value was tied to integrating provider availability from Underpin Health, the external clinic system, so that a quote reflects real free dates and an accepted booking writes back to the clinic diary automatically. Both were explicitly placed after current scope.

## Operational Direction

### MTG-003-P01: Admin dashboard access for stakeholders

Stakeholder access to the Admin dashboard was requested and agreed. Access uses the same entry point as the Provider dashboard with role-separated accounts.

### MTG-003-P02: Stakeholder website review

Stakeholders will review all published pages, with treatment hub pages called out specifically as the pages still lacking supplied content.

### MTG-003-P03: Immediate project-team follow-ups

Named as follow-up work in the meeting: export the translation key list to the stakeholder side; continue reviewing the treatment and package catalogs in both Admin and Provider; review the payments brief received the prior week; and prepare the corresponding mobile designs so the app team can update the affected flows.

## Open Questions

### MTG-003-O01: Final shape of the reduced quote flow

Which steps merge, and whether treatment selection and treatment-date selection become one step, was not settled. Five steps is the design target to work toward rather than a fixed number to hit, so the resulting step count is settled by the grouping design.

### MTG-003-O02: Provider quoting volume

Whether providers routinely quote at a volume that would justify quote duplication was not established. Stakeholders asked for provider input before revisiting MTG-003-D04.

### MTG-003-O03: Translation activation and cost

Whether automatic translation is switched on at launch, which fields it covers, and what the cost ceiling is were not decided.

### MTG-003-O04: Payout confirmation window

The automatic release window remains unset between 48 and 72 hours. This repeats MTG-002-D08 and MTG-002-O02 and is still open.

### MTG-003-O05: Website publication set

Which pages are published at launch and which stay in draft was left to a later decision.

## Validation Needed

- Confirm participant names and stakeholder roles; only phonetic first names were available from the transcript.
- Confirm Turkish as the sole first-phase language and the intended second language.
- Verify the reported status items against implementation before reuse, in particular the untested billing backend and the inactive translation capability.

## Requirement Routing for Later Work

| Items | Likely owner | Current action |
|---|---|---|
| MTG-003-D01, D03, O01 | FR-004 and provider quote-flow UX | Change Request required before implementation; five steps is a design target, not an acceptance criterion |
| MTG-003-D02 | FR-004 and pricing model contracts | Constraint to verify against current schema |
| MTG-003-D04, O02 | Provider quoting scope | Record only; no build |
| MTG-003-D05, D06, D07, O03 | Localization contract, messaging, and inquiry free-text fields | Material reconciliation required; needs an owning contract |
| MTG-003-D08, D09, P02 | Website and design work | Not a PRD update |
| MTG-003-D10, D11, O04 | FR-007, FR-017, FR-029, and the payments brief (SRC-DOC-001) | Reconcile together with SRC-DOC-001 |
| MTG-003-F01 | Roadmap | Record only; explicitly deferred |
| MTG-003-P01, P03 | Project team | Operational follow-up |

## Relationship to Earlier Sources

- The revised quote hierarchy under "Reported Status" is the implementation of SRC-MTG-002 items D03 to D06 and O01, already incorporated through `CR-FR004-20260909-01`, `CR-FR005-20260915-01`, and `CR-FR006-20260915-01`. This meeting reported its status and did not reopen it.
- MTG-003-O04 restates the unresolved confirmation window from MTG-002-D08 and MTG-002-O02.
- MTG-003-D10 and D11 depend on the payment structure described in SRC-DOC-001, which remains pending review.
