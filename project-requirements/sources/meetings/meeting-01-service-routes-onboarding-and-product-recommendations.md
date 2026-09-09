---
source_id: SRC-MTG-001
source_type: stakeholder-meeting
meeting_date: not-provided
captured_on: 2026-09-09
validation_status: pending-review
incorporation_status: not-incorporated
---

# Meeting 01: Service Routes, Onboarding, and Product Recommendations

## Context

The meeting reviewed proposed next-phase mobile designs, missing service routes, onboarding, monitoring, aftercare, and product recommendations. The supplied evidence was a rough transcript attached outside the repository. It was intentionally not copied into the project because it contains conversational noise and unrelated discussion.

Participant names and roles require confirmation. The discussion appears to include Hairline stakeholders, the project lead, and the product designer.

## Confirmed Directions

### MTG-001-D01: Four service routes

The mobile experience should support four recognizable patient routes:

1. Get a hair transplant through Hairline.
2. Monitor hair loss.
3. Monitor progress after a transplant performed outside Hairline.
4. Request standalone aftercare.

The transplant route already existed. The other routes required new or refined entry experiences.

### MTG-001-D02: Initial onboarding needs a reset

The splash screen, pre-registration explanation, onboarding sequence, and first service-selection step should be redesigned as one coherent entry flow. The opening experience should explain what the app offers before asking a user to register or provide personal data.

The existing male-model splash image was not considered an effective representation of the product. A scan-oriented or otherwise more representative visual direction was preferred.

### MTG-001-D03: Release flows and future recommendations must be designed together

The service routes required for release should be designed first, while leaving deliberate room for product recommendations so the same screens do not need to be redesigned shortly after launch.

Product recommendation was described as a post-launch capability rather than a launch blocker. The discussion used approximately three months after release as an example, not a committed delivery date.

### MTG-001-D04: Aftercare and product recommendation are separate services

Aftercare means managed post-procedure support: provider-specific instructions, milestones, scans, symptom monitoring, escalation, and clinical follow-up. General product recommendation addresses longer-term hair and scalp support and may apply before or after surgery. One must not be presented as the other.

### MTG-001-D05: Patients may move between service routes

Monitoring should provide a controlled path into another relevant service when the patient changes intent. Examples discussed were hair-loss monitoring converting to a transplant inquiry and transplant-progress monitoring converting to standalone aftercare.

## Working Models Requiring Detailed Review

### MTG-001-W01: Hair-loss monitoring modes

The proposed working model allows one active hair-loss monitoring case and offers:

- self-monitoring at a patient-chosen cadence; or
- limited provider-supported monitoring assigned through Admin.

The patient may record scans, observations, a short note, and a severity value. In provider-supported mode, an assigned provider periodically reviews activity and posts advice. Admin assigns a provider and handles reassignment if the provider withdraws.

The meeting expressed overall agreement with the direction, but did not finalize every cadence, scoring, clinical-safety, assignment, or communication rule.

### MTG-001-W02: External transplant-progress monitoring

The proposed route is self-service for a transplant performed outside Hairline. It tracks progress without automatically assigning a provider. The patient may complete the monitoring case or request standalone aftercare.

### MTG-001-W03: Standalone aftercare activation

The proposed flow creates an aftercare request, allows Admin to assign a suitable provider, lets that provider configure the care plan, and activates managed aftercare after successful payment.

### MTG-001-W04: Monitoring value and shareable progress

Recurring standardized scans and month-to-month comparison were identified as the core value of monitoring. A shareable visual comparison was suggested as a possible acquisition mechanism, but its format, consent model, privacy controls, and release scope were not settled.

## Open Questions

### MTG-001-O01: Recommendation interaction

Should tailored recommendations use an AI conversation, a structured questionnaire, or another guided interaction? The meeting requested exploration of multiple design options.

### MTG-001-O02: Recommendation safety and scoring

It remains undecided whether severity is patient-entered, system-assisted, or assessed through an AI capability. Any AI grading, medical interpretation, or treatment recommendation requires a separate clinical-safety and product decision.

### MTG-001-O03: Product selection and commercial model

The meeting did not decide:

- which products may be recommended;
- whether recommendations come from Hairline inventory, partners, affiliates, or external retailers;
- how commercial relationships are disclosed;
- how the system avoids presenting care guidance as an advertisement; or
- whether a marketplace is needed.

### MTG-001-O04: Product ownership by route

The discussion suggested generic products for users without an active case, provider-selected products during managed treatment, and questionnaire/data-informed products during self-monitoring. This allocation was not finalized.

## Future Directions

### MTG-001-F01: Medical and prescription pathway

Country-specific clinician consultations and prescription fulfilment were described as a valuable future capability, potentially six to twelve months after release. This was explicitly not a day-one feature and depends on regulatory and operational systems not resolved in the meeting.

### MTG-001-F02: Marketing and product analytics

The stakeholder described future marketing attribution, creator/affiliate activity, and operational dashboards. This was contextual business direction, not a detailed requirement approved by this meeting.

## Requirement Routing for Later Work

| Items | Likely owner | Current action |
|---|---|---|
| MTG-001-D02 | FR-001 and design work | Record only |
| MTG-001-D01, D05, W01 | FR-037 and system workflow | Record only |
| MTG-001-D01, D05, W02 | FR-038 and system workflow | Record only |
| MTG-001-D04, W03 | FR-011 | Record only |
| MTG-001-D03, O01-O04, F01 | Future product-recommendation scope | No owning FR selected |
| MTG-001-F02 | Product and marketing planning | Not a PRD update |

## Validation Needed

- Confirm the meeting date, participant names, and stakeholder roles.
- Confirm that the five items marked as confirmed directions reflect the meeting outcome.
- Confirm whether each working model was accepted for detailed design or only presented for discussion.
- Resolve the open questions before translating them into product requirements.
