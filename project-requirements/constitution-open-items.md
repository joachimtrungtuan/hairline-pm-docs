# Constitution: remaining technical points

Stateful list, not an authority. The owner ruled on 2026-11-25 and `constitution.md` was corrected (version 1.1.0; the change log names each rule). Closed by that ruling, one line each:

- Retention: `C-II-4`, `C-SEC-14` (one 10-year period; the Appendix "7-year" text is marked superseded).
- Minimum Android version: `C-IV-1` (Android 10+).
- MFA: `C-SEC-23`, with `C-II-8` unchanged (future feature, not enforced at launch).
- Patient identity before payment: `C-II-2`, `C-SEC-9`, `C-SEC-10`, `C-SEC-11` (system PRD wording).
- Affiliate application: `C-I-0`, `C-I-0a`, Part D Tenant 4 (fourth application).
- Lockout: `C-SEC-21` (admin setting, default 5 attempts and 15 minutes).
- Mobile load time: `C-VIII-2` (under 3 seconds).
- Module naming and scope notes: Principle VII and the Part D tenant lists.
- Hard deletion: `C-VI-11` (new; every delete is soft); the summary-only statements stay in the Appendix as history.
- Archived data: `C-SEC-16` (both halves stated).
- Aftercare priority: Part D tenant lists and Appendix (P1, first release).
- Part C versus `graph/checklists/prd-structure.md`: `C-PRD-1`, `C-PRD-6` to `C-PRD-12`, `C-PRD-14`, `C-PRD-25` to `C-PRD-28`; the canonical templates directory replaces the FR-011 template statement.
- Summary-only items (NON-NEGOTIABLE on Principle VI, numeric targets, table count): the original governs; not carried as rules.
- Tenant 3 "Security Settings" fixed password policy and OTP length: no change (it matches the system PRD).

## Remaining technical points (for the development team, no owner decision needed)

Evidence class for each: comparison with `system-prd.md` or the archived technical documents in `local-docs/archived/technical-docs/`.

1. Web stack. Tenants 2 and 3 say "React/Vue.js + Laravel"; the archived technical spec has the heading "Framework: React 18 + Vite". Mobile stack is "to be decided" in both.
2. Coverage thresholds. The CI pipeline step "minimum 70% for critical paths" is lower than C-DEV-18 "Critical user flows ... 90%+ coverage".
3. Vendor and tool names baked into rules (xe.com in C-IX-4, Stripe, Redis/SQS, Plane/Jira) may be stale; not verified.
4. Part D layout trees are stale: "91 tables" (the old summary said 97, the archived data schema says 117), and the future-structure folders (`system-design/`, `api-specs/`, `security/`) were not checked against the current tree.

Controller question:

- Whether the duplicate module list (Principle VII and the Appendix) and the full tenant lists should become pointers in a later pass.

Notes from the merge review (2026-11-25):

- In the original, the documentation placement "Rules" list (now `C-DOC-2` to `C-DOC-8`) and the layout trees sat under the heading "PRD Standards & Requirements (NON-NEGOTIABLE)". In the restructured file they sit under their own heading. A note there says the NON-NEGOTIABLE status of the original heading still covers them; the owner may confirm or lift it.
- `C-GOV-6` says "Update to Sync Impact Report". The Spec Kit sync-report comment that opened the original file was dropped in the restructure (its facts are in the change log), so this step has nothing to update unless the comment is restored.
- The old summary said "real-time exchange rates"; the original does not. Not carried as a rule.
- Rule ids were also given to some lines that state targets and carry no MUST (for example `C-VIII-1` to `C-VIII-9`); the ids are citation labels only.
