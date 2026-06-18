# Sprint 3 Readiness & Fix Backlog

---

## Document Control & Sprint Summary

| Field | Value |
|---|---|
| Sprint | Sprint 3 |
| Theme | Peripheral: Messaging, Notifications & Additional Config |
| Dates | June 8 (Mon) - June 12 (Fri), 2026 · 5 working days |
| Working days | 5 |
| Goal | Verify and complete all communication infrastructure, notification configuration, and supporting admin config that wraps around the core platform flow. |
| Definition of Done | All Sprint 3 modules pass QA on staging; no open critical bugs on any Sprint 3 module; cumulative regression QA over Sprint 1 + Sprint 2 modules completed on staging with no open critical bugs; production Stripe environment configured and verified end-to-end (live keys loaded, webhook secret encrypted, test deposit transaction processed); website design complete and development at 80%+; beta build successfully submitted to Apple TestFlight and Google Play internal track with no store rejection. |
| Source launch plan | `local-docs/product-plans/2026-05-13/launch-plan.md` |
| Prepared by | Claude AI agent |
| Prepared date | 2026-06-14 |
| Product review date(s) | Not performed in this pass; this report scaffolds the Sprint 3 scope and readiness backlog from the launch plan. |
| Product environment(s) checked | No staging, production, local build, or app build was checked in this pass. |
| Review scope boundary | Source review only. Scope, DoD, modules, stories, deferrals, and readiness gaps are derived from the Sprint 3 section of the launch plan. Product defects must be added after real staging/product review with evidence links. |

<!--
AI agent guidance: Keep this guidance hidden from Markdown preview. It exists only to preserve the intended workflow for future agents editing this report.

## How To Use This Template

- Section 1 mirrors the launch plan. Do not add new scope, reinterpret the sprint, or silently move work between sprints.
- Section 2 is the working fix backlog. Capture issues found from real product review in enough detail that the dev team can reproduce and fix them quickly. Rows marked as evidence gaps are not confirmed product bugs; they are required product-review checks that must be backed by staging evidence before Sprint 3 can be treated as complete.
- Section 3 is for findings that should not distract the current sprint. Use it to prevent out-of-scope issues from being treated as sprint commitments.
- Do not include Plane ticket IDs, assignees, estimates, or ownership fields. Those belong to the later Plane-ticket creation workflow.

### Priority Scale

| Priority | Meaning |
|---|---|
| P0 | Blocks sprint completion, staging validation, or a core end-to-end journey. |
| P1 | Major required feature gap or broken required flow for this sprint. |
| P2 | Required but contained issue that does not block the whole sprint. |
| P3 | Minor UX, copy, polish, or cleanup issue that should not block sprint completion. |

-->

# 1. Sprint Scope From Launch Plan

## 1.1 Modules In Scope

| Surface | Module | FR / Scope Notes | Launch Plan Reference |
|---|---|---|---|
| Patient Mobile | P-06 Communication | FR-012 patient-side: in-app messaging with provider, media attachments, audio/video call initiate/receive. | Sprint 3 Modules |
| Patient Mobile | P-08 Help Center & Support Access | FR-035 Patient Help & Support: help articles, FAQ browse, support ticket submission. | Sprint 3 Modules |
| Cross-tenant (Patient + Provider) | P-02 / PR-06 Reviews & Ratings | FR-013: patient post-treatment review submission, provider response surface (admin moderation in A-01/A-10). | Sprint 3 Modules |
| Patient Mobile | P-03 Promotion Code Application | FR-019 patient-side checkout: code entry, single-discount enforcement, discount summary. | Sprint 3 Modules |
| Patient Mobile | P-01 Language & Privacy/DSR Surfaces | FR-021 patient-side runtime switch + seeded bundle fetch (before RC freeze); FR-023 patient privacy/retention surfaces + deletion request status. | Sprint 3 Modules |
| Provider Web | PR-07 Communication & Messaging | FR-012 provider-side: chat, media attachments, outgoing audio/video call initiation, conversation history. | Sprint 3 Modules |
| Provider Web | PR-06 Help Centre & Support Access | FR-032 Provider Dashboard Settings; FR-033 Help Centre Management; FR-034 Support Center Ticketing. | Sprint 3 Modules |
| Provider Web | PR-02 / PR-05 Discount Participation | FR-019 provider-side: quote/booking discount context, provider-created discounts, accept/decline platform-shared discounts. | Sprint 3 Modules |
| Admin Web | A-06 Discount & Promotion Management | FR-019 admin-side: three program types, approval workflow, single-discount-per-booking enforcement, usage reporting. | Sprint 3 Modules |
| Admin Web | A-09c System Settings & Payment Rules — Part 2 | FR-020 Notifications & Alerts; FR-030 Notification Rules Configuration; FR-031 Admin Access Control (templates, rules, admin team management, role/permission config). | Sprint 3 Modules |
| Admin Web | A-09 Help Centre Content Management | FR-033 admin authoring: patient/provider article taxonomy, publish/version/audit. | Sprint 3 Modules |
| Admin Web | A-10 Communication Monitoring & Support | FR-012 monitoring + FR-034: keyword flagging, thread monitoring, emergency intervention with mandatory reason logging, support case lifecycle/escalation. | Sprint 3 Modules |
| Admin Web | A-01 Reviews Moderation | FR-013 admin-side: takedown request queue, removal for policy violations, authenticated review insertion. | Sprint 3 Modules |
| Shared Service | S-03 Notification Service | FR-020 delivery infrastructure: push/email/in-app delivery, throttling, retry, bounce handling, delivery tracking. | Sprint 3 Modules |

## 1.2 User Stories In Scope

### Patient

- As a patient, I want to send/receive messages with my assigned provider in-app, including photos and documents, so that quote/treatment questions stay in the secure thread.
- As a patient, I want to initiate and receive audio/video calls with my provider in-app, so that I can have face-to-face consultations without a separate tool.
- As a patient, I want to browse organised Help Center articles and search FAQs, so that I can self-serve answers at any stage.
- As a patient, I want emergency contact/help to remain visible and article helpfulness feedback captured.
- As a patient, I want to submit a support ticket with category, attachments, and contact preference, then reply, reopen eligible cases, and see closure/auto-close status.
- As a patient who completed treatment, I want to submit a rating, review text, and photos, so that I can share my experience.
- As a patient, I want to flag a review or response that violates platform policy.
- As a patient, I want to apply one valid promotion/provider/affiliate code at checkout and see the final discount before payment, so that pricing is transparent and stacking is prevented.
- As a patient, I want to switch app language from settings and have it remembered across sessions and devices (before the RC mobile freeze).
- As a patient, I want to view privacy/retention policy info, submit a deletion/erasure request, and track its status/outcome.

### Provider

- As a provider, I want to send messages, attach media, and initiate audio/video calls with patients from the dashboard.
- As a provider, I want patient conversation threads grouped by patient and treatment context (FR-022 messaging search/filter deferred).
- As a provider, I want to browse provider-specific Help Centre articles, submit a support case, reply to admin follow-ups, and track case status.
- As a provider, I want to create my own eligible discounts and accept/decline platform-shared discounts before they go live for my clinic.
- As a provider, I want to view reviews left by my patients and post one response per review.

### Admin

- As an admin, I want promotion creation to follow the FR-019 program model (Admin-via-Provider, Provider Self-Created, Hairline-Funded & Direct-Issued).
- As an admin, I want the platform to enforce single-discount-per-booking and produce live applied/completed reporting.
- As an admin, I want to configure notification templates with variables and multi-language content.
- As an admin, I want to configure notification delivery rules per event and channel (push/email/in-app).
- As an admin, I want to invite, suspend, assign built-in/custom roles, prevent last-Super-Admin lockout, sync linked provider permission rules, and audit every effective permission change.
- As an admin, I want to manage separate patient/provider Help Centre repositories with category, publish state, version history, and audit trail.
- As an admin, I want automatic keyword flagging on message threads with a configurable keyword list.
- As an admin, I want to intervene in a patient↔provider thread under a "Hairline Admin" badge with mandatory reason logging.
- As an admin, I want patient/provider support tickets to support reply, follow-up, reopen, auto-close, escalation, reassignment, and priority changes with reason tracking.
- As an admin, I want to review takedown requests and remove policy-violating reviews with reason logged and patient notified.
- As an admin, I want to insert authenticated reviews on behalf of verified offline patients (elevated audit trail).

### Shared Services / Platform Foundations

- As any platform user, I want push, email, and in-app notifications delivered reliably and in real time.
- As an admin, I want delivery telemetry (sent / delivered / failed / bounced) per channel.

### Affiliate / Partner

- No affiliate or partner module is assigned to Sprint 3.

## 1.3 Explicitly Deferred / Out Of Scope

| Item | Launch Plan Reason / Destination | Notes |
|---|---|---|
| FR-012 messaging search/filter | Deferred — FR-022 P2 post-MVP | Conversation history grouping ships; search/filter does not, unless reprioritised. |
| Patient provider-discovery search | Deferred — P2 post-MVP | Sprint 3/4 search scope excludes patient provider discovery. |
| Admin DSR actioning | Deferred to Sprint 4 (A-01 / A-09c / S-06) | Sprint 3 ships patient-side language/privacy/DSR surfaces; admin actioning follows. |
| A-09c Part 3 (i18n & compliance authoring) | Deferred to Sprint 4 | Only A-09c Part 2 (notifications, team, roles) is Sprint 3 scope. |
| Full in-app invoice/receipt history archive | Out of launch scope per FR-017 backlog | Carry-over deferral from Sprint 2. |

---

# 2. Sprint Fix Backlog

## 2.1 Sprint-Level Blockers

| Bug ID | Priority | Area | Issue | Steps to Reproduce | Actual Outcome | Expected Outcome | Evidence Link | Task Status | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  | P0 | Sprint QA evidence | Sprint 3 cannot be closed from this report alone because no staging QA evidence is attached for all Sprint 3 modules. | 1. Open this report.<br>2. Review Document Control and module sections.<br>3. Check for staging/build evidence links. | No product environment was checked in this pass. | Each Sprint 3 module has staging QA evidence and clear pass/fail status. | TBD | Review pending | Readiness blocker, not a confirmed product defect. |
|  | P0 | Cumulative regression (Sprint 1 + 2) | Cumulative regression QA over Sprint 1 + Sprint 2 modules must complete on staging with no open critical bugs; not yet evidenced. | 1. Re-run Sprint 1 + Sprint 2 flows on staging.<br>2. Capture pass/fail evidence per area. | No regression evidence is attached in this report. | Sprint 1 + 2 areas still pass alongside Sprint 3 additions. | TBD | Review pending | Direct Sprint 3 DoD gate; required before Sprint 4 final regression. |
|  | P0 | Production Stripe verification | Production Stripe must be configured and verified end-to-end (live keys, encrypted webhook secret, test deposit processed); not yet evidenced. | 1. Load live Stripe keys + webhook secret in production config.<br>2. Process a test deposit transaction.<br>3. Confirm webhook delivery and audit entry. | Production Stripe verification was not checked in this pass. | Production Stripe is verified end-to-end before Sprint 4 final regression. | TBD | Review pending | Carry-forward dependency into Sprint 4 readiness. |
|  | P1 | Beta build submission | Beta build must be submitted to Apple TestFlight and Google Play internal track with no store rejection; not yet evidenced. | 1. Submit beta build to TestFlight.<br>2. Submit to Google Play internal track.<br>3. Confirm no rejection. | Beta submission status was not checked in this pass. | Beta builds accepted on both tracks. | TBD | Review pending | Non-dev Sprint 3 milestone (June 11). |
|  | P1 | Website design/dev milestone | Website design complete and development at 80%+; not yet evidenced. | 1. Confirm website design completion.<br>2. Confirm development progress ≥80%. | Website status was not checked in this pass. | Website meets the Sprint 3 design/dev milestone. | TBD | Review pending | Non-dev Sprint 3 milestone (June 12). |

## 2.2 Module Fix Backlog

## P-06 - Communication (patient-side)

### Review Notes

- Checked areas: Launch-plan scope only.
- Current state: Product behavior not checked in this pass.
- Review limits: Requires staging review of in-app messaging, media attachments (virus scan), Twilio audio/video, read receipts, and delivery state.

### Remaining Fixes

| Bug ID | Priority | Flow / Story | Issue | Steps to Reproduce | Actual Outcome | Expected Outcome | Evidence Link | Task Status | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  | P1 | Patient messaging & calls | Evidence gap: patient messaging, media attachments, and audio/video calls have not been verified in staging. | Send/receive text + media with the assigned provider, then initiate and receive a Twilio audio/video call with permission flows; verify read receipts/timestamps/delivery state. | Not reviewed in this pass. | Messaging, attachments (virus-scanned), and calls work per FR-012 patient-side. | TBD | Review pending | Patient-support and aftercare-team messaging stay in FR-034/FR-011. |

## P-08 - Help Center & Support Access

### Review Notes

- Checked areas: Launch-plan scope only.
- Current state: Product behavior not checked in this pass.
- Review limits: Requires staging review of article browse, FAQ search, emergency contact visibility, ticket submission/lifecycle, and helpfulness feedback.

### Remaining Fixes

| Bug ID | Priority | Flow / Story | Issue | Steps to Reproduce | Actual Outcome | Expected Outcome | Evidence Link | Task Status | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  | P1 | Help & support lifecycle | Evidence gap: help browse/search and the patient support-ticket lifecycle have not been verified in staging. | Browse articles by category, search FAQs, submit a ticket with attachments, reply, reopen an eligible case, and confirm only published content shows. | Not reviewed in this pass. | Help content, FAQ search, emergency contact, and full ticket lifecycle work per FR-035/FR-033/FR-034. | TBD | Review pending | Help content reflects A-09 published state only. |

## P-02 / PR-06 - Reviews & Ratings (cross-tenant)

### Review Notes

- Checked areas: Launch-plan scope only.
- Current state: Product behavior not checked in this pass.
- Review limits: Requires staging review of patient review submission, eligibility window (3 months), immediate publish, provider single response, and feed into A-01/A-10.

### Remaining Fixes

| Bug ID | Priority | Flow / Story | Issue | Steps to Reproduce | Actual Outcome | Expected Outcome | Evidence Link | Task Status | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  | P1 | Reviews & ratings | Evidence gap: review submission, eligibility, and provider response have not been verified in staging. | Submit a post-treatment review (rating + text + photo) once eligible, confirm immediate publish and one-per-treatment guardrail, and post a single provider response. | Not reviewed in this pass. | Submission, eligibility, publish, and provider response work per FR-013 and feed A-01/A-10. | TBD | Review pending | Added to Sprint 3 scope. |

## P-03 - Promotion Code Application

### Review Notes

- Checked areas: Launch-plan scope only.
- Current state: Product behavior not checked in this pass.
- Review limits: Requires staging review of checkout code entry, discount summary, and rejection of invalid/expired/stacked codes.

### Remaining Fixes

| Bug ID | Priority | Flow / Story | Issue | Steps to Reproduce | Actual Outcome | Expected Outcome | Evidence Link | Task Status | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  | P1 | Checkout promotion code | Evidence gap: promotion code application and single-discount enforcement have not been verified in staging. | Enter a valid code at checkout, confirm discount value/source/final amount, then attempt invalid/expired/second-stacked codes. | Not reviewed in this pass. | Valid code applies with clear summary; invalid/expired/stacked codes rejected with reason per FR-019. | TBD | Review pending | Patient-side surface of A-06 programs. |

## P-01 - Language & Privacy/DSR Surfaces

### Review Notes

- Checked areas: Launch-plan scope only.
- Current state: Product behavior not checked in this pass.
- Review limits: Requires staging review of language selector persistence, runtime bundle fetch + fallback, privacy/retention content, and deletion-request status.

### Remaining Fixes

| Bug ID | Priority | Flow / Story | Issue | Steps to Reproduce | Actual Outcome | Expected Outcome | Evidence Link | Task Status | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  | P1 | Patient language & DSR | Evidence gap: language switching and patient privacy/DSR surfaces have not been verified in staging before RC freeze. | Switch language and confirm persistence across sessions/devices + runtime re-render with fallback; view privacy/retention content; submit a deletion request and view status. | Not reviewed in this pass. | Language switch, server-side locale recording, policy content, and DSR status work per FR-021/FR-023 (admin actioning is Sprint 4). | TBD | Review pending | Must land before the RC mobile freeze. |

## PR-07 - Communication & Messaging (provider-side)

### Review Notes

- Checked areas: Launch-plan scope only.
- Current state: Product behavior not checked in this pass.
- Review limits: Requires staging review of provider messaging, media, outgoing Twilio calls, and conversation history grouping.

### Remaining Fixes

| Bug ID | Priority | Flow / Story | Issue | Steps to Reproduce | Actual Outcome | Expected Outcome | Evidence Link | Task Status | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  | P1 | Provider messaging & calls | Evidence gap: provider messaging, attachments, and outgoing audio/video call initiation have not been verified in staging. | Send/receive messages + media with a patient, initiate an outgoing Twilio audio/video call, and confirm conversation history by patient/treatment context. | Not reviewed in this pass. | Provider messaging, attachments, and outgoing calls work per FR-012 provider-side. | TBD | Review pending | Messaging search/filter is deferred (FR-022 P2). |

## PR-06 - Help Centre & Support Access (provider-side)

### Review Notes

- Checked areas: Launch-plan scope only.
- Current state: Product behavior not checked in this pass.
- Review limits: Requires staging review of provider article browse/search, support case lifecycle, and account deletion/support request path.

### Remaining Fixes

| Bug ID | Priority | Flow / Story | Issue | Steps to Reproduce | Actual Outcome | Expected Outcome | Evidence Link | Task Status | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  | P1 | Provider help & support | Evidence gap: provider help browse/search and support-case lifecycle have not been verified in staging. | Browse/search provider Help Centre articles, submit a support case, read admin replies, send a follow-up, and submit an account deletion/support request. | Not reviewed in this pass. | Provider help and support lifecycle work per FR-032/FR-033/FR-034. | TBD | Review pending | Admin approval routes through A-10/A-02. |

## PR-02 / PR-05 - Discount Participation (provider-side)

### Review Notes

- Checked areas: Launch-plan scope only.
- Current state: Product behavior not checked in this pass.
- Review limits: Requires staging review of provider-created discounts, accept/decline platform-shared discounts, and provider usage summary.

### Remaining Fixes

| Bug ID | Priority | Flow / Story | Issue | Steps to Reproduce | Actual Outcome | Expected Outcome | Evidence Link | Task Status | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  | P1 | Provider discount participation | Evidence gap: provider discount creation and accept/decline of shared discounts have not been verified in staging. | Create a provider-owned discount where permitted, accept/decline a platform-shared discount before activation, and view active discounts + usage summary. | Not reviewed in this pass. | Provider discount creation, accept/decline, and usage visibility work per FR-019. | TBD | Review pending | Feeds A-06 program model. |

## A-06 - Discount & Promotion Management

### Review Notes

- Checked areas: Launch-plan scope only.
- Current state: Product behavior not checked in this pass.
- Review limits: Requires staging review of three program types, approval workflow, single-discount enforcement, and live usage reporting.

### Remaining Fixes

| Bug ID | Priority | Flow / Story | Issue | Steps to Reproduce | Actual Outcome | Expected Outcome | Evidence Link | Task Status | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  | P1 | Discount program management | Evidence gap: A-06 program creation, approval, enforcement, and reporting have not been verified in staging. | Create each of the three FR-019 program types, exercise the provider-acceptance approval workflow, confirm single-discount-per-booking enforcement, and check live usage reporting. | Not reviewed in this pass. | All three program types, approval, no-stacking enforcement, and live reporting work per FR-019. | TBD | Review pending | Usage reporting must use live data, no mocks. |

## A-09c - System Settings & Payment Rules (Part 2)

### Review Notes

- Checked areas: Launch-plan scope only.
- Current state: Product behavior not checked in this pass.
- Review limits: Requires staging review of notification templates/rules, admin team management, and role/permission (RBAC) configuration.

### Remaining Fixes

| Bug ID | Priority | Flow / Story | Issue | Steps to Reproduce | Actual Outcome | Expected Outcome | Evidence Link | Task Status | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  | P1 | Notifications, team & roles | Evidence gap: A-09c Part 2 notification config and admin RBAC have not been verified in staging. | Configure notification templates (variables, EN/TR) and delivery rules; invite/suspend admins; assign built-in/custom roles; confirm last-Super-Admin lockout prevention, Effective From tracking, and immutable audit entries. | Not reviewed in this pass. | Templates, rules, team management, and RBAC enforcement work per FR-020/FR-030/FR-031. | TBD | Review pending | A-09c Part 3 (i18n/compliance) is Sprint 4. |

## A-09 - Help Centre Content Management

### Review Notes

- Checked areas: Launch-plan scope only.
- Current state: Product behavior not checked in this pass.
- Review limits: Requires staging review of article CRUD/publish/version, audience targeting, and audit logging.

### Remaining Fixes

| Bug ID | Priority | Flow / Story | Issue | Steps to Reproduce | Actual Outcome | Expected Outcome | Evidence Link | Task Status | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  | P1 | Help content authoring | Evidence gap: Help Centre article authoring and audience targeting have not been verified in staging. | Create/edit/publish/unpublish/version articles for patient and provider audiences and confirm P-08/PR-06 only show published content for the correct audience with audit logging. | Not reviewed in this pass. | Authoring, taxonomy, audience targeting, and audit logging work per FR-033. | TBD | Review pending | Gates P-08 and PR-06 help content correctness. |

## A-10 - Communication Monitoring & Support

### Review Notes

- Checked areas: Launch-plan scope only.
- Current state: Product behavior not checked in this pass.
- Review limits: Requires staging review of keyword flagging, monitoring dashboard, emergency intervention with reason logging, and support case lifecycle on live data.

### Remaining Fixes

| Bug ID | Priority | Flow / Story | Issue | Steps to Reproduce | Actual Outcome | Expected Outcome | Evidence Link | Task Status | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  | P1 | Monitoring & intervention | Evidence gap: keyword flagging, emergency intervention, and support lifecycle have not been verified in staging. | Trigger keyword flagging on a thread, post an admin intervention under the "Hairline Admin" badge with mandatory reason, and exercise the full support case lifecycle on live data. | Not reviewed in this pass. | Flagging, intervention-with-reason, and support lifecycle work per FR-012 monitoring/FR-034 on live data. | TBD | Review pending | All screens must use live data, no mocks. |

## A-01 - Reviews Moderation

### Review Notes

- Checked areas: Launch-plan scope only.
- Current state: Product behavior not checked in this pass.
- Review limits: Requires staging review of takedown queue, policy removal with notification, and authenticated review insertion.

### Remaining Fixes

| Bug ID | Priority | Flow / Story | Issue | Steps to Reproduce | Actual Outcome | Expected Outcome | Evidence Link | Task Status | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  | P1 | Reviews moderation | Evidence gap: takedown queue, removal, and authenticated insertion have not been verified in staging. | Surface a flagged review in the takedown queue, remove it for policy violation with reason logged and patient notified, and insert an authenticated review on behalf of a verified offline patient. | Not reviewed in this pass. | Takedown, removal-with-reason, and authenticated insertion work per FR-013 with elevated audit trail. | TBD | Review pending | Added to Sprint 3 scope. |

## S-03 - Notification Service

### Review Notes

- Checked areas: Launch-plan scope only.
- Current state: Product behavior not checked in this pass.
- Review limits: Requires staging review of push/email/in-app delivery, throttling, retry, bounce handling, and delivery telemetry.

### Remaining Fixes

| Bug ID | Priority | Flow / Story | Issue | Steps to Reproduce | Actual Outcome | Expected Outcome | Evidence Link | Task Status | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  | P0 | Notification delivery infrastructure | Evidence gap: end-to-end push/email/in-app delivery and telemetry have not been verified in staging. | Trigger events across channels; confirm FCM/APNS push, SMTP email with bounce handling, and in-app centre with read state/throttling/retry; review delivery telemetry (sent/delivered/failed/bounced). | Not reviewed in this pass. | All channels deliver with tracking per FR-020; admin can view delivery telemetry. | TBD | Review pending | Unblocks deferred delivery verification from Sprint 1 and Sprint 2 events. |

---

# 3. Not For This Sprint

| Item | Why It Is Not In This Sprint | Follow-Up Notes |
|---|---|---|
| FR-012 messaging search/filter | Deferred — FR-022 P2 post-MVP | Conversation grouping ships; search/filter does not unless reprioritised. |
| Patient provider-discovery search | Deferred — P2 post-MVP | Not part of launch search scope. |
| Admin DSR actioning | Deferred to Sprint 4 (A-01 / A-09c / S-06) | Sprint 3 ships patient-side DSR surfaces only. |
| A-09c Part 3 (i18n & compliance authoring) | Deferred to Sprint 4 | Only A-09c Part 2 belongs to Sprint 3. |
| Full in-app invoice/receipt history archive | Out of launch scope per FR-017 backlog | Carry-over deferral. |
