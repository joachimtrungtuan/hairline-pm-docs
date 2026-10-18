# MTG-002 Quote Model — End-of-Session Note and Handoff

**Date**: 2026-10-18
**Update Type**: End-of-session note (status, open items and handoff for the next session; no document changes)
**Related Update Log**: [MTG002_QUOTE_MODEL_ALIGNMENT_2026-10-16.md](../2026-10-16/MTG002_QUOTE_MODEL_ALIGNMENT_2026-10-16.md)
**Decision Log**: `reports/2026-10-16/mtg002-quote-model-decisions-2026-10-16.md`

Read this first if you are picking up the MTG-002 quote/subquote work in a new session. It covers what the work is, where it stands, the rules to follow, and what is left. Paths are relative to `local-docs/`.

## 1. Where we are (one paragraph)

The documentation work for the MTG-002 quote and subquote data model is **complete and committed**. Every affected PRD, its Change Request, the three system documents, the decision log, the fix plan and the update log are consistent with each other as of 2026-10-18. The working tree in `local-docs` was clean after the last change commit (`501c0d8`); this note was added afterwards. Nothing has been pushed. What remains is (a) one small open product question, (b) the separate **payment pass**, which was deliberately kept out of scope, and (c) optional housekeeping. Section 6 lists them.

## 2. Scope of the work

- **In scope:** the quote/subquote data model introduced by Meeting 02 (`project-requirements/sources/meetings/meeting-02-launch-quote-options-fund-release-and-payments.md`). The hierarchy is: Inquiry, then Parent Quote, then Quote Option (up to 5), then option × date-price row. One option × one date row is a **subquote**, and the patient accepts exactly one subquote per inquiry. The scope also covers every consumer of that model: acceptance record and snapshot, slot hold, booking handoff, Payment Window Expired, provider-fault handling, promotions, commission base, notifications, admin screens, analytics, and the schema.
- **Out of scope (reference only):** payment rails, payout and fund release, refunds, cancellation fee economics, later-instalment handling, and Meeting 03. These belong to the **payment pass** (Section 6.2).

## 3. Key documents (all paths relative to `local-docs/`)

| Document | Role |
|---|---|
| `reports/2026-10-16/mtg002-quote-model-decisions-2026-10-16.md` | **Authoritative decision log.** It holds every Product Owner decision: D1–D24, D6-M, R7-1 to R7-4, M1–M18, P1–P3 and Q1–Q50, plus the "Controller defaults" paragraph at the end. Read this before changing anything. |
| `reports/2026-10-16/mtg002-quote-model-fix-plan-2026-10-16.md` | Approved fix plan. Its status line says the work is executed, with the consolidated verification and final audit complete. |
| `reports/2026-10-16/mtg002-quote-model-verification-2026-10-16.md` | The original verification report (findings that started the work). |
| `project-requirements/functional-requirements/frNNN-*/prd.md` | The PRDs (21 affected). |
| `project-requirements/functional-requirements/frNNN-*/change-request-2026-10-16-mtg002-quote-model-alignment.md` | One MTG-002 Change Request per affected PRD (21 in total), with IDs of the form `CR-FRNNN-20261016-01`. |
| `project-requirements/system-data-schema.md`, `system-technical-spec.md`, `system-prd.md` | The system documents. |
| `project-requirements/update-logs/2026-10-16/MTG002_QUOTE_MODEL_ALIGNMENT_2026-10-16.md` and `update-logs/README.md` | The update log for this whole change set, with its README entries. |

The detailed audit reports (f1 lifecycle, f2 money, f3 notifications and roles, f4 data, f5 document control) and the agent briefs lived in a temporary job folder that is deleted when the session ends. **Do not look for them.** Every finding was either fixed or turned into a decision row in the decision log.

## 4. What was done (chronological)

1. **Verification and decisions (2026-10-16):** a concurrent cross-FR verification found 4 Critical, 45 Major, 87 Minor and 24 Observation findings. The Product Owner decided every Critical and Major finding (D-, M-, P- and R-series).
2. **Fix waves 0–4 and a light audit (2026-10-16):** the PRDs, the new CRs and the system docs were aligned.
3. **Q-series Q1–Q30 (2026-10-16):** open questions raised during the waves were answered and applied. Q26 and Q27 were deferred to the payment pass.
4. **Consolidated verification (2026-10-18):** one pass re-checked every file and fixed residual inconsistencies.
5. **Final independent business-analysis audit (2026-10-18):** a five-area audit (lifecycle, money, notifications and roles, data, document control) led to decisions Q31–Q44 and their fixes.
6. **Round 2 (2026-10-18):** gaps found while applying the fixes led to decisions Q45–Q50, which were applied in the same 2026-10-18 versions (no further version bump).
7. **Records:** the decision log, fix plan, update log and README were refreshed, and the work was committed.

### Main rules now in force (see the decision log for exact wording)

**Acceptance and money**
- **Acceptance:** acceptance creates an immutable AcceptanceEvent snapshot and a fixed slot hold.
- **Payment Window Expired:** applies to the first payment only. An admin can revive the booking with a fresh hold.
- **Booking total:** after promotion, the one base for deposit, instalments and commission. Commission is snapshotted at booking confirmation and may be a Percentage or a Flat Rate.

**Cancellation**
- **Patient:** can cancel only before acceptance (stages Inquiry and Quoted). From acceptance onward the patient is routed to admin support.
- **Admin:** only an admin cancels a booking, from any booking state, with a mandatory reason and an audit entry. The booking and the inquiry become Cancelled, and the accepted quote stays `accepted` (Q37).

**Provider fault**

| When it happens | What happens |
|---|---|
| Before treatment (Accepted or Confirmed) | The booking closes and the inquiry stays open with `supportRequired`. The admin authors a replacement quote in the same inquiry (FR-004 Workflow 7 and Screen 8). This is the only exception to the block on new quotes after acceptance. The replacement acceptance inserts one supersession record (Q35). The replacement quote gets no automatic promotion (Q48), expires normally if it is not accepted (Q49), and is excluded from provider analytics (Q50). |
| In Progress | The booking stays In Progress with `supportRequired`, and the admin decides case by case on FR-006 Screen 11 (Alternative Flow B7). The admin either moves the booking to Aftercare and reassigns the aftercare provider, or cancels it (Q45). |
| Aftercare | The admin reassigns the aftercare provider only, on FR-011 Screen 19, and `aftercare.provider_reassigned` is sent. There is no new acceptance or payment (Q36, Q47). |

**Admin screens**
- Every admin intervention has an admin screen (Q43):
  - revive, appointment change, cancellation and provider-fault transfer (FR-006);
  - replacement quote (FR-004);
  - treatment-detail change (FR-010);
  - aftercare reassignment (FR-011);
  - booking support requests (FR-016);
  - Hairline share % on promotion set-up (FR-019).

**Treatment**
- **Treatment details:** the clinic can change them until Check In. An admin can change them at any time from Confirmed onward, with a reason, an audit entry and `treatment.plan_changed` (Q44).
- **Treatment record:** created at booking confirmation in state Awaiting Check In (Q46).

**Promotions**
- **Storage:** new `promotion_programs` and `promotion_codes` tables; `discounts` is legacy (Q38).
- **Automatic promotions:** one per quote (Q40), with one reservation per quote, consumed at acceptance.
- **Provider-selected promotions and patient codes:** reserved at acceptance and consumed at first payment.
- **Release reasons:** these include `not_applied` (Q39).
- **Both Fees:** carries a per-promotion Hairline share % (Q41).

**Notifications**
- **`booking.scheduled`:** goes to the patient only and is mandatory.
- **`booking.rescheduled`:** new; FR-006 is the producer; goes to the patient and provider and is mandatory (Q42).
- **`aftercare.provider_reassigned`:** new and mandatory (Q47).
- **`quote.withdrawn`:** the admin is told only after acceptance (Q31).
- **Admins:** get exception alerts only.
- **Mandatory provider notices:** cannot be suppressed by preferences.

## 5. Final versions and commits

| Document | Version |
|---|---|
| FR-003 | v2.11 |
| FR-004 | v3.4 |
| FR-005 | v2.8 |
| FR-006 | v2.10 |
| FR-007 | v1.10 |
| FR-007b | v1.5 |
| FR-008 | v2.9 |
| FR-010 | v2.5 |
| FR-011 | v1.5 |
| FR-014 | v3.18 |
| FR-015 | v1.20 |
| FR-016 | v1.9 |
| FR-017 | v2.14 |
| FR-019 | v2.5 |
| FR-020 | v2.10 |
| FR-022 | v2.17 |
| FR-024 | v1.5 (unchanged in the final pass) |
| FR-026 | CR only in the final pass |
| FR-029 | v1.14 |
| FR-030 | v1.15 |
| FR-032 | v1.12 |
| System data schema | 1.11.0 |
| System technical spec | 1.4.0 |
| System PRD | 1.2.0 |

**Commits in `local-docs`, oldest first** (`main` branch, not pushed):

- First round:
  - `3523886` reports
  - `84117b7` quotes
  - `ff91a5f` booking
  - `d7b4cfe` payments
  - `4342532` notifications
  - `811255c` system
  - `886f2cf` update logs
- Final round:
  - `d8565b1` reports
  - `b411ad3` quotes
  - `bea4e4f` booking
  - `06a9e29` promotions
  - `8e8e828` notifications
  - `611b0bf` system
  - `501c0d8` update logs

## 6. What is left to do

### 6.1 Open product question (small, needs the Product Owner)

- **Treatment record state after an In Progress provider fault moves the booking to Aftercare.** FR-006 Alternative Flow B7 lets the admin move the booking to Aftercare, but no document says whether the treatment record ends as `completed` or `cancelled`. Ask the Product Owner, then update FR-010 (treatment record states), FR-006 (B7), and the schema's `treatment_records` status rules. Log it as Q51 in the decision log.

### 6.2 Payment pass (the next major piece of work; not started)

These items were explicitly parked:

- **Q26:** admin cancellation after a missed later instalment.
- **Q27:** the provider payout trigger.
- Refunds and cancellation fees, including for the new admin-only cancellation from any state and for provider-fault cases.
- Payments that have no `booking_id`.
- FR-029 Rule 6 (missed instalment handling).
- The instalment minimum expressed in USD.
- Whether Hairline reimburses anything for Hairline-only promotions beyond the commission effect.
- FR-034 (support case types): it may need booking-cancellation and booking-change case types to back the FR-016 Booking Support Requests screen. This was noted but not changed.

### 6.3 Optional housekeeping

- The CRs still say `**Related Commit(s)**: Pending`. Fill them with the commit hashes in Section 5 if the user wants that traceability.
- Push `local-docs` only if the user asks.

## 7. Rules the next agent must follow

**Project rules** (from `CLAUDE.md`; read it and `local-docs/INDEX.md` first)
- **Work area:** `local-docs/` is the only work area.
- **NEVER EDIT** `main/` (the dev source code). Do not open `main/` unless the user explicitly asks.
- **FROZEN:** `project-automation/skills-engineering/`, `commands/`, `workflows/` and `task-prompt/`.
- **Root config** (`CLAUDE.md`, `AGENTS.md`, `.gitignore`) needs two-step approval to edit.

**Token rules**
- Start at `local-docs/INDEX.md`.
- Never read a PRD whole. List headings with `rg -n "^#{1,4} " file`, then read only the section you need.
- Cap content searches with `rg -n -m 20`.
- Do not read update logs or git history by default. Use `git diff --stat` or `--name-only`, never a bare `git diff` or `git log`.

**Editing conventions**
- No literal `|` inside Markdown table cells, and no `\|` either.
- Keep table column counts intact.
- Decision IDs (Q5, D6, M18 and the like) appear only in Change Log rows, CRs and approval tables, never in requirement body text.
- Each edited PRD gets a minor version bump, a Change Log row, an updated footer "Last Updated" date and an amended CR.

**Update logs and commits**
- Significant changes need an update-log entry plus README updates (date section, topic entries and "Last Updated").
- Commits use conventional format, focused per area, with **no AI attribution and no Co-Authored-By line** (the user's rule).

**Working with the Product Owner (the user)**
- Ask product decisions through AskUserQuestion, offering a recommended option.
- Record every answer straight away as a new row in the decision log.
- Never reverse a recorded decision without asking.
- Write in English (NZ). Timezone is Asia/Saigon.

## 8. Suggested first step for the next session

Read Section 6, then ask the user which to do: settle the open treatment-record question (6.1), start the payment pass (6.2), or do the housekeeping (6.3). For the payment pass, start from the decision log rows Q26 and Q27 and the parked list above, and follow the same pattern: verify, then decide with the Product Owner, then fix, then audit, then commit.
