# Phase {N} Manual Test Guide — {Phase Name}

> **Template.** Copy this file to `testing/manual/v{N}/phases/{phase-folder}/test-guide.md`, then replace every `{placeholder}`. Remove this note in the copy. Phase scope, objective, and exit gate stay in the product plan (`product-plans/v{N}/plan.md`); this guide holds test content only. Rules: `testing/TEST-STRATEGY.md`.

## Document Control

| Field | Value |
|---|---|
| Phase | Phase {N} — {Phase Name} |
| Plan version | v{N} |
| Guide version | {1.0} |
| Status | {Draft / Active / Superseded} |
| Product plan | {Relative link to product-plans/v{N}/plan.md and the phase section} |
| Created | {YYYY-MM-DD} |
| Last updated | {YYYY-MM-DD} |
| Guide owner | {Name / role} |
| Tester(s) | {Name(s)} |

## Change Log

| Version | Date | Change | By |
|---|---|---|---|
| {1.0} | {YYYY-MM-DD} | Initial guide | {Name} |

## 1. Test Scope

Phase scope, release objective, and exit gate are owned by the product plan (Document Control › Product plan). This section maps that scope to test batches.

### 1.1 In Scope

| Module | Function slice in this phase | FRs | Batch |
|---|---|---|---|
| {PR-01} | {What is tested in this phase} | {FR-002, FR-031} | {B01} |

### 1.2 Out of Scope

- {Deferred function and the phase it belongs to}

## 2. Entry and Exit Criteria

**Entry criteria** (all must hold before testing starts):

- {Build deployed to the test environment; version recorded below}
- {Test accounts available and verified}

**Exit criteria** (phase passes when):

- Every High-priority case is Pass.
- No open bug (Bug status Found, Logged, Fixed - retest, or Reopened) on a High-priority case.
- {Exit gate items for this phase, one bullet each, quoted from the product plan}

## 3. Test Environment and Accounts

| Item | Value |
|---|---|
| Provider dashboard URL | https://admin.hairline.app (shared origin with the admin dashboard; sign in with a provider account) |
| Admin dashboard URL | {URL} |
| Backend API base URL | {URL} |
| Build / release under test | {Version or date} |
| Browser(s) | {Chrome latest, desktop} |

Accounts used (placeholders; credentials sent privately):

| Placeholder | Role | Used in batches |
|---|---|---|
| {V1} | {Provider owner} | {B01, B02} |

## 4. Batches and Run Order

| Order | Batch | File | Module | FRs | Cases | Depends on |
|---|---|---|---|---|---|---|
| 1 | {B01} | [{B01-pr01-slug}](batches/{B01-pr01-slug}.md) | {PR-01} | {FR-002} | {12} | {—} |

**End-to-end journey:** {One paragraph describing how the batches chain into the phase's business journey, so the tester sees the whole flow before testing parts.}

## 5. Test Runs and Progress

Progress is recorded per test run, not in this guide. Each run is a folder `results/run-NN-YYYY-MM-DD/` with one result copy per batch and a `summary.md` holding that run's Progress Summary. The `manual-test-bug-sync` skill creates the run (`new-run`), merges returned results, and refreshes the summary. Never fill in the scaffolds in `batches/`. Rules: TEST-STRATEGY §2 and §7.
