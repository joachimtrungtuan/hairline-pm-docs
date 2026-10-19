# Phase {N} Manual Test Plan — {Phase Name}

> **Template.** Copy this file to `testing/manual/phases/{phase-folder}/v{major}.0/plan.md`, then replace every `{placeholder}`. Remove this note in the copy. Rules: `testing/TEST-STRATEGY.md`.

## Document Control

| Field | Value |
|---|---|
| Phase | Phase {N} — {Phase Name} |
| Plan version | {1.0} |
| Status | {Draft / Active / Superseded} |
| Scope source | {Roadmap path and section} |
| Release objective | {From roadmap} |
| Exit gate | {From roadmap} |
| Created | {YYYY-MM-DD} |
| Last updated | {YYYY-MM-DD} |
| Plan owner | {Name / role} |
| Tester(s) | {Name(s)} |

## Change Log

| Version | Date | Change | By |
|---|---|---|---|
| {1.0} | {YYYY-MM-DD} | Initial plan | {Name} |

## 1. Scope

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
- {Roadmap exit gate items for this phase, one bullet each, quoted from the release roadmap}

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

## 5. Progress Summary

Update after each test session (the `manual-test-bug-sync` skill can refresh this).

| Batch | Total | Pass | Fail | Blocked | Not tested | Open bugs | Last tested |
|---|---|---|---|---|---|---|---|
| {B01} | {12} | 0 | 0 | 0 | {12} | 0 | — |
| **Total** | | | | | | | |
