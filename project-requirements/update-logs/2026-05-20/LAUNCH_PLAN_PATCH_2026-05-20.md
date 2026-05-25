# Launch Plan Patch — May 20, 2026

**Type:** Document Revision
**File:** `local-docs/product-plans/2026-05-13/launch-plan.md`
**Prepared By:** Product Manager

---

## Summary

Five coordinated patch groups applied to the Hairline Platform Launch Plan: (1) the entire timeline shifted one week later to account for an operational delay that prevented Sprint 1 from starting on the originally planned May 14 date; (2) all aftercare modules moved from Sprint 1 to Sprint 2 to group them with the configuration and template setup they depend on; (3) user stories added to all four sprint sections as a business-level testing and alignment aid; (4) implementation-readiness corrections applied after PRD cross-check; (5) a lightweight Sprint Zero prep window and earlier Sprint 1 start were added to reflect the current preparation cadence.

---

## Patch 1 — Full Timeline Shift (+7 Days)

**Reason:** Operational problems prevented Sprint 1 from starting on May 14 as originally planned. Sprint 1 planning now occurs on May 20 (today, PM solo). Development begins May 21 (Thu). Sprint 1 Kickoff ceremony moves to May 22 (Fri) per PM preference.

**Changes:**
- Sprint 1: May 14–22 → **May 21–29** (Kickoff: May 22 Fri)
- Sprint 2: May 25–29 → **June 1–5**
- Sprint 3: June 1–5 → **June 8–12**
- Sprint 4: June 8–12 → **June 15–19**
- Launch: June 15–16 → **June 22–23**
- All ISO dates in Mermaid Gantt blocks shifted +7 days
- All day-by-day schedule tables updated to new dates
- All non-dev milestone dates updated
- Risk register dates updated
- App Store and Website Timeline Gantt dates updated
- Ceremony cadence row updated: Sprint 1 planning noted as Wed May 20 (day before dev begins)
- Document header updated: Date → May 20, 2026; Target Go-Live → June 22–23, 2026

**App Store timeline adjustments (within the shift):**
- Beta Build Submission: June 4 → June 11
- Final Build Submission: June 9 → June 16
- Store Approval Window: June 10–14 → June 17–21

**Website timeline adjustments (within the shift):**
- Website Finalization & Staging: 4 days (June 15–18)
- DNS Pre-Check: June 18, 1 day
- Website Go-Live: June 22

**Sprint 1 inner Gantt special case:** Dev bar starts May 21 (+7 days); Kickoff milestone stays May 22 (+8 days) because the PM explicitly chose Friday for the kickoff ceremony.

---

## Patch 2 — Aftercare Modules Moved from Sprint 1 → Sprint 2

**Reason:** Aftercare modules (P-05, PR-04, A-03) depend on aftercare templates (A-09b) and system settings (A-09c), which are Sprint 2 items. Grouping all aftercare setup in Sprint 2 prevents a split dependency and keeps the activation journey coherent.

**Modules moved:**
- P-05 Aftercare & Progress Monitoring (Patient mobile)
- PR-04 Aftercare Participation (Provider dashboard)
- A-03 Aftercare Team Management (Admin dashboard)

**Sprint 1 changes:**
- Sprint calendar theme: "Core: Inquiry, Quote, Treatment & Aftercare" → **"Core: Inquiry, Quote & Treatment"**
- Sprint 1 goal updated to note aftercare deferred to Sprint 2
- P-05, PR-04, A-03 removed from Sprint 1 module list
- Deferred note added beneath Sprint 1 modules listing the three moved modules and the rationale
- Sprint 1 DoD: removed A-03, PR-04, P-05, P-05b bullets; journey statement updated to end at treatment check-in with note "aftercare activation verified in Sprint 2"

**Sprint 2 changes:**
- Sprint calendar theme: "Config: Quoting Rules & Payment Sub-features" → **"Config & Aftercare: Quoting Rules, Payment Sub-features & Aftercare Activation"**
- Sprint 2 section heading updated to match
- Sprint 2 goal updated: adds aftercare activation across all three tenants as a third theme
- P-05, PR-04, A-03 added to Sprint 2 module list with sub-feature descriptions
- Sprint 2 DoD: six new acceptance criteria bullets added for P-05, PR-04, and A-03

---

## Patch 3 — User Stories Added to All Sprint Sections

**Reason:** User stories provide a business-level view of what each sprint delivers, making them useful for testing planning, team alignment, and stakeholder communication — especially for non-technical participants who find functional requirements too granular.

**Format:** "As a [role], I want [action], so that [benefit]." Stories are grouped by user role (Patient, Provider, Admin, Platform Foundations) and placed in a `## User Stories` section immediately after each sprint's Definition of Done.

**Sprints updated:**
- Sprint 1: 12 user stories covering P-01, P-02, P-03a, P-07, PR-01, PR-02, PR-03, A-01, A-02, A-09a, S-01, S-02, S-05
- Sprint 2: 10 user stories covering P-03b, P-04, P-05, PR-04, PR-06, A-03, A-09b, A-09c, S-04
- Sprint 3: 8 user stories covering P-06, P-08, PR-07, A-06, A-09c (Part 2), A-10, S-03
- Sprint 4: 6 user stories covering PR-05, A-04, A-05, A-07, A-08, S-06

---

## Patch 4 — Implementation-Readiness Corrections After PRD Cross-Check

**Reason:** Follow-up review found timeline, FR/module mapping, DoD, and integrated-story issues that would make the launch plan unsafe as an implementation baseline. FR-036 is intentionally not fixed into current scope because the detailed FR-036 PRD is not composed yet; it remains an acknowledged future placeholder only.

**Changes:**
- Clarified soft-launch/public-store relationship: June 22–23 remains vendor-facing soft launch; public store release is triggered only if approvals land in time, otherwise vendor demos proceed through approved beta/internal distribution.
- Added launch-scope authority notes for draft launch PRDs (FR-018, FR-021, FR-023, FR-035) and explicit FR-036 exclusion from Sprint 4 delivery scope.
- Corrected Sprint 1 mappings: A-01 now includes admin oversight for FR-003/004/005/006; FR-026 ownership moved to A-09a while P-01 remains a consumer of policy/reason lists.
- Corrected payment dependencies: Sprint 1 deposit uses a launch-default deposit rate; admin-editable FR-029 deposit rules remain Sprint 2; S-02 no longer owns provider/admin payout/refund UI surfaces.
- Corrected Sprint 1 treatment-execution sequencing: Sprint 1 verifies treatment execution against a fully-paid staging fixture, while the real patient final-balance path that unlocks check-in is delivered in Sprint 2.
- Corrected notification timing: Sprint 1/2 now generate visible events/states where needed, while full push/email/in-app delivery is verified in Sprint 3 under S-03.
- Corrected travel mapping: provider travel surface moved from PR-02 wording to PR-04 booking-detail context; Sprint 4 admin travel is embedded oversight/exception handling, not a standalone travel dashboard.
- Corrected FR-019 mapping and taxonomy: provider discount participation now maps to PR-02/PR-05, and A-06 uses the FR-019 program model (Admin-via-Provider, Provider Self-Created, Hairline-Funded & Direct-Issued).
- Corrected FR-012 messaging boundary: patient-provider messaging remains FR-012; support tickets and aftercare communication stay in FR-034/FR-035 and FR-011 respectively; deferred messaging search/filter remains FR-022 P2.
- Expanded FR-035 Help/Support DoD to include emergency contact visibility, ticket replies/reopen/auto-close status, content-type coverage, and helpfulness feedback.
- Expanded FR-031, FR-021, and FR-023 DoD coverage for RBAC safeguards, localization shared-service dependencies, provider compliance visibility, DSR notifications, compliance exports, and patient DSR status handling.
- Moved patient-side i18n/privacy/DSR surfaces into Sprint 3 so mobile-code work lands before the June 16 RC freeze; patient language switching uses seeded launch translation bundles until Sprint 4 admin authoring/publish/rollback controls are delivered.
- Added integrated launch user stories covering end-to-end inquiry/payment/treatment/aftercare, zero-quote intervention, cancellation/refund, support/messaging boundaries, affiliate attribution-to-payout, compliance/i18n/search, and store-fallback readiness.

---

## Patch 5 — Sprint Zero Added; Sprint 1 Start Advanced

**Reason:** A lightweight preparation window is needed before delivery work begins so the team can finish soft-launch planning and task setup. Sprint 1 planning therefore moves to May 18, and Sprint 1 development starts on May 19 while the rest of the launch schedule remains unchanged.

**Changes:**
- Added **Sprint Zero** to the launch-plan overview and Sprint Calendar: **May 11–15, 2026**
- Added a short preparation note clarifying Sprint Zero is for soft-launch planning and task setup only
- Updated the Master Timeline Mermaid block to include a **Sprint Zero · Preparation** section
- Moved Sprint 1 PM planning from **May 20 → May 18**
- Moved Sprint 1 development start from **May 21 → May 19**
- Moved Sprint 1 kickoff from **May 22 → May 20** to preserve the kickoff-after-start cadence
- Updated the Sprint 1 heading, internal Gantt, App Store account-setup start date, and day-by-day schedule to match the new Sprint 1 opening dates
- Clarified the general sprint-planning cadence note so Sprint 1 is explicitly documented as the post-Sprint-Zero exception

---

## Source Documents

- `local-docs/product-plans/2026-05-13/launch-plan.md` — patched in place
- `local-docs/project-requirements/update-logs/2026-05-14/LAUNCH_PLAN_PATCH_2026-05-14.md` — previous patch entry
