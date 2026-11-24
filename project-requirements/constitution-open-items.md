# Constitution: open items for the owner

Written 2026-11-25 (Asia/Saigon) during the constitution consolidation. The restructure changed no rule wording. The points below looked outdated, or disagree between the original constitution, the old executive summary, `system-prd.md` and `graph/checklists/prd-structure.md`. None was resolved; each waits for an owner ruling. This file is a stateful list, not an authority: remove an item once it is ruled.

## List (a): rules in the original that look outdated or wrong (not changed)

Evidence class for each: comparison with `system-prd.md` (Platform-Wide Rules, NFR) or `system-technical-spec.md` headings.

1. Retention. C-II-4 and C-SEC-14: medical records 7 years; C-SEC-17: audit trails 10 years. `system-prd.md` "One 10-year retention period" says every record type, including medical records, is kept 10 years and no type has a shorter period.
2. Minimum Android version. C-IV-1: "iOS 14+ and Android 8.0+". `system-prd.md` NFR-006: "iOS 14+, Android 10+".
3. MFA contradicts itself. C-II-8 says MFA is a planned control, not yet enforced, with interim controls. C-SEC-23 says MFA MUST be enforced for all Admin users and provider admin accounts. `system-prd.md` NFR-003 says the system MUST support MFA for providers and admins.
4. Patient identity before payment. C-SEC-10 shows "Mark P #A47B2"; `system-prd.md` shows "Mark P." followed by the ID, and exempts admins. C-II-2 says "until treatment is confirmed and paid", C-SEC-9 says "until booking is confirmed and paid", the PRD says "until booking confirmation (the first successful payment)". Same intent, three wordings.
5. Affiliate surface. C-I-0a says the Affiliate Portal is not a fourth tenant. `system-prd.md` "System Architecture" says "four distinct applications" including an Affiliate Platform.
6. Web stack. Tenants 2 and 3 say "React/Vue.js + Laravel"; `system-technical-spec.md` heading "Framework: React 18 + Vite". Mobile stack is "to be decided" in both.
7. Lockout versus admin settings. C-SEC-21 fixes lockout at 5 attempts and 15 minutes; Tenant 3 "Security Settings" lists authentication throttling (max login attempts, lockout duration) as admin settings. `system-prd.md` "Core security controls fixed in code" leans to fixed. Unresolved which governs.
8. Coverage thresholds. The CI pipeline step "minimum 70% for critical paths" is lower than C-DEV-18 "Critical user flows ... 90%+ coverage".
9. Mobile load time. C-IV-4 (loading states under 3 seconds, p95) and C-VIII-2 (core screens under 2 seconds on 4G) are two thresholds for similar things; `system-prd.md` NFR-001 says under 3 seconds.
10. Module naming. Principle VII lists S-01 "3D Scan Processing Service" and P-07 "3D Scan Capture & Viewing"; the summary and PRD use head scan media (V1 photo set, V2 true 3D).
11. Tenant 3 "Security Settings" (original 590 to 593, FIXED password policy and OTP length 6) is rule-like but sits in descriptive text, so it has no id. It matches `system-prd.md` "Password and one-time-code policy".
12. Vendor and tool names baked into rules (xe.com in C-IX-4, Stripe, Redis/SQS, Plane/Jira): may be stale; not verified.
13. Part D layout trees (stale): "91 tables" (summary says 97, `system-data-schema.md` says 117), and the future-structure folders (`system-design/`, `api-specs/`, `security/`) were not checked against the current tree.

## List (b): disagreements, not resolved

Original versus summary:

1. Principle VI: the summary heads it "(NON-NEGOTIABLE)"; the original does not (original NON-NEGOTIABLE: I, II, V and PRD Standards). The summary heading "10 Non-Negotiable + Essential" does not match either.
2. Hard deletion: the summary adds "HARD DELETES STRICTLY PROHIBITED: System MUST NOT allow hard deletion of any medical, financial, or patient data" and "Soft-deletes ONLY ... (7-year minimum ...)". The original has C-VI-4 (soft deletes on medical/booking data) and C-II-5 / C-SEC-15 (archival). `system-prd.md` "Soft deletes only" states hard deletion prohibited for every delete. Kept verbatim in the Appendix, not in Part A.
3. Archived data: summary "Archived data MUST remain accessible for compliance audits"; original C-SEC-16 "Archived data MUST be inaccessible via normal application interfaces". Not necessarily opposite (audit access versus normal interface) but not reconciled.
4. Module lists: the summary adds priorities, renames S-01 and P-07 and S-04 (MVP travel record storage, Phase 2 APIs), S-05 (V1/V2 media), PR-02 (includes Appointment Management & Pre-scheduling). Original lists have none of this.
5. Aftercare priority: summary A-03 Aftercare Team Management is P1 and the Phase 2 list also names "Aftercare Management (all tenants)"; the original Admin Tenant item 3 says P2. Summary P-05 "Aftercare & Progress Monitoring" is P1, original Tenant 1 item 6 "Aftercare & Monitoring" is P2.
6. Affiliate: summary "Affiliate Platform (lightweight sub-module)"; original C-I-0a "operated as part of the Admin Platform tenant".
7. MFA: summary says "MFA for Admin and Provider platforms" as in force; original C-II-8 says planned.
8. Numbers only in the summary: "80%+ test coverage across codebase", "95%+ Constitution compliance", "Zero critical vulnerabilities", "every 2-week sprint"; these do not appear in the original.
9. Table count: tree in original 91, in summary 97.

Original PRD Standards (Part C) versus `graph/checklists/prd-structure.md` v1.0:

1. C-PRD-8 Success Criteria (REQUIRED): the checklist drops success metrics from the compressed PRD (frozen baseline only).
2. C-PRD-10 Assumptions (REQUIRED): the checklist drops assumptions after moving embedded rules to Business Rules.
3. C-PRD-11 Implementation Notes (REQUIRED): the checklist drops technical notes after a completeness re-check.
4. C-PRD-9 Dependencies with three kinds (internal, external, data): the checklist reduces them to one list of related FR ids.
5. C-PRD-12 Completeness, "All sections MUST be fully populated": cannot hold while the sections in items 1 to 3 are removed.
6. The original does not name User Scenarios and Testing, Functional Requirements Summary, edge cases, Change Log or Approvals; the compressed structure (`local-docs/INDEX.md` section C.1) has them.
7. Business Rules: the original lists four rule groups; the checklist says each rule is stated once and cited by REQ id. Additive, not contradictory.
8. Traceability: original "Every requirement MUST reference source FR and module codes"; the checklist adds graph field ids per field row. Additive.
9. Template: the original names the FR-011 PRD as the definitive template; the project instructions name `local-docs/project-requirements/templates/` as the canonical template directory. Which governs for new PRDs is not stated in either.
10. Header fields (C-PRD-2) were not compared against the compressed PRD header; not checked.

## Open questions for the controller

1. Version number after a restructure with no rule change (kept 1.0.0 with a "Structure revised" line).
2. Whether the duplicate module list (deviation 2) and the full tenant lists (deviation 3) should become pointers in a later pass, once the owner rules on list b.
3. The new file points readers to this report (stateful) from its header; remove that sentence once the owner has ruled on the open items.

## Added by the merge review (2026-11-25)

- In the original, the documentation placement "Rules" list (now `C-DOC-2` to `C-DOC-8`) and the layout trees sat under the heading "PRD Standards & Requirements (NON-NEGOTIABLE)". In the restructured file they sit under their own heading. A note there says the NON-NEGOTIABLE status of the original heading still covers them; the owner may confirm or lift it.
- `C-GOV-6` says "Update to Sync Impact Report". The Spec Kit sync-report comment that opened the original file was dropped in the restructure (its facts are in the change log), so this step has nothing to update unless the comment is restored.
- The old summary said "real-time exchange rates"; the original does not. Not carried as a rule.
- Rule ids were also given to some lines that state targets and carry no MUST (for example `C-VIII-1` to `C-VIII-9`); the ids are citation labels only.
