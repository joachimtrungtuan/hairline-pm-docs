# Hairline Web E2E Testing Constitution

**Version:** 1.2
**Status:** Approved; subject to evidence-driven amendment
**Created:** 2026-07-11
**Governed scope:** Provider Dashboard and Admin Dashboard web E2E testing
**Architecture:** `local-docs/testing-automation/ARCHITECTURE.md`

---

## Preamble

This constitution governs Hairline's living web end-to-end testing system. It protects three things simultaneously:

1. repeatable, token-free automated execution;
2. traceability to the live Hairline requirements and module structure;
3. human authority over bugs, requirement interpretation, and test maintenance.

The architecture explains the system design. This constitution defines the rules that every registered case, runtime component, result, review action, and AI-assisted maintenance workflow must follow.

This constitution is the active governance baseline. It is expected to improve through evidence gathered during pilot and later test runs, but every amendment remains subject to Article 14.

## Article 1 — Authority and Scope

### 1.1 Human decision authority

Only a human reviewer may:

- confirm that a result is a product bug;
- approve the owning function or flow, its operational boundaries, and its canonical happy path;
- approve a changed expected outcome;
- accept a frontend discrepancy against a requirement;
- classify a result as requiring a test update;
- retire or supersede a registered case;
- close, defer, duplicate, verify, or reopen a review item;
- authorize creation of an external bug or implementation task.

The deterministic runner and AI agents may collect evidence, assign objective preliminary labels, and make proposals. Their outputs are advisory and never final product decisions.

### 1.2 Delegated PRD-derived case authority

Once a human approves a function or flow and its canonical happy path, that approval delegates registration authority for the complete set of non-happy cases that are directly and unambiguously derived from the governing PRDs. The registration agent may create, revise, controlled-validate, and activate those derived cases without requesting separate approval for every case.

Delegated authority applies only when the expected behavior follows directly from an approved source requirement, business rule, validation rule, permission rule, state transition, or documented alternative flow. It does not permit the agent to invent product behavior or resolve product ambiguity.

The agent must stop for human direction when:

- authoritative sources conflict or leave the expected outcome ambiguous;
- the live UI/API diverges from the source and choosing a new baseline requires product judgment;
- a required account state or synthetic-data mutation is destructive, externally consequential, or lacks prior authority;
- a case cannot be executed safely or deterministically;
- a proposed case changes the approved happy-path boundary rather than testing it.

Human authority over issue classification, bug confirmation, intentional frontend discrepancies, changed expected outcomes, case retirement, and external work-item creation remains unchanged.

### 1.3 Initial governed surfaces

This constitution initially governs:

- Provider Dashboard web functions and flows;
- Admin Dashboard web functions and flows;
- the Hairline development environment;
- deterministic API-assisted synthetic-data preparation;
- Playwright browser verification against the real development frontend and backend;
- SQLite execution and human-review history;
- filesystem screenshots, traces, downloads, and diagnostic artifacts.

Mobile automation, load testing, backend unit testing, and API contract testing remain outside this initial scope.

### 1.4 Change control

Changes to this constitution require explicit human approval and a recorded revision. No test run, AI recommendation, frontend change, or source-document change may silently alter its rules.

## Article 2 — Source-of-Truth Contract

### 2.1 Locate through the index

Registration and review work must start at `local-docs/INDEX.md` and narrow to the relevant source document and section before reading or changing testing material.

### 2.2 Authoritative sources

Depending on the case, authoritative sources may include:

- `local-docs/project-requirements/system-prd.md`;
- a functional PRD under `local-docs/project-requirements/functional-requirements/`;
- a product plan under `local-docs/product-plans/`.

The relevant source document remains authoritative for its own subject. A test registry entry is never a replacement PRD.

The live development APIs may be inspected to understand implemented contracts, prepare deterministic test data, and diagnose discrepancies. API behavior is implementation evidence; it does not automatically override the expected product behavior defined by the PRDs.

### 2.3 No requirement duplication

Registered cases must reference live source paths, requirement identifiers, and headings. They must not copy whole requirements, business-rule tables, module definitions, or PRD narratives into the registry.

The registry may record only the test-specific interpretation required to execute a case:

- preconditions;
- dataset recipe;
- UI interaction mapping;
- observable assertions;
- approved implementation notes or discrepancies;
- automation references.

### 2.4 Source-change review

Each approved case must be associated with source-section hashes or an equivalent stable change-detection mechanism.

If a referenced source changes:

- the case receives `SOURCE_REVIEW_REQUIRED`;
- the currently approved test definition may continue to run;
- the result enters `NEEDS_HUMAN_REVIEW`, even if its functional assertions pass;
- no expected outcome, locator, step, or dataset changes automatically.

Formatting-only changes should not trigger requirement review where a stable normalization method can safely distinguish them.

## Article 3 — Classification and Traceability

### 3.1 Module-first organization

The existing Hairline module IDs are the primary classification system. Every registered function, flow, case, dataset, run result, artifact, and review record must resolve to one primary module.

### 3.2 Cross-module flows

A cross-module flow has one primary owning module and one or more participating-module relationships. It must not be copied into multiple module folders as separate competing definitions.

### 3.3 Stable identifiers

The implementation must define stable identifiers for:

- modules;
- functions;
- flows;
- test cases;
- datasets;
- test runs;
- case executions;
- attempts;
- artifacts;
- human reviews;
- case revisions.

An identifier remains stable when its description or implementation mapping changes. A materially different behavior receives a new identifier or an explicitly approved superseding relationship.

### 3.4 Required trace chain

Every execution must be traceable through this chain:

```text
source references
  → registered case revision
  → dataset recipe revision and runtime seed
  → test run and attempt records
  → generated backend records
  → evidence artifacts
  → human review decision
  → related bug/fix/re-test, when applicable
```

## Article 4 — Registered Case Contract

### 4.1 Required case content

Every active registered case must include or resolve:

- stable case ID and title;
- primary and participating modules;
- function or flow ID;
- test level;
- scenario category;
- regression tier or priority;
- live source references;
- preconditions;
- deterministic data recipe;
- current approved UI actions;
- observable assertions;
- automation script and test-name reference;
- registry status;
- last UI-confirmed date;
- monotonic revision.

### 4.2 Test levels

The supported levels are:

- `function` — one function or rule with isolated prerequisites;
- `module-flow` — an internal journey within one primary module;
- `cross-module-flow` — one business journey across multiple modules.

### 4.3 Scenario categories

Cases may be classified as:

- happy path;
- negative or validation;
- boundary or edge;
- permission or role;
- state transition;
- idempotency;
- concurrency-sensitive;
- data consistency;
- another human-approved category.

### 4.4 Registry lifecycle

The minimum registry statuses are:

- `DRAFT`;
- `ACTIVE`;
- `SOURCE_REVIEW_REQUIRED`;
- `UI_REVIEW_REQUIRED`;
- `UPDATE_APPROVED`;
- `SUPERSEDED`;
- `RETIRED`.

Only `ACTIVE` cases are included in ordinary selection by default. Review-required cases may continue to run against their last approved definition but must be surfaced to humans.

### 4.5 Two-stage registration gate

Test registration must separate high-level flow alignment from detailed case work:

1. **PRD flow scout:** locate the relevant PRD through `local-docs/INDEX.md`, read only the module scope and overall business-flow sections needed to understand the journey, and return a concise flow outline, boundaries, and unresolved questions.
2. **Human happy-path approval:** stop and wait for the Product Owner to correct, supplement, and approve the function/flow boundary and canonical happy path.
3. **Complete derived-suite registration:** after happy-path approval, inspect detailed requirements, screens, live UI/API behavior, roles, datasets, alternatives, validations, boundaries, permissions, and state transitions. Derive and register the complete applicable suite without separate per-case approval when Article 1.2 applies.
4. **Coverage and execution proof:** document requirement-to-case coverage, controlled-validate every case, and activate unambiguous PRD-derived cases whose execution reaches a meaningful pass/fail assertion. Route every non-clean outcome to human review.

The PRD flow scout must not generate a full case matrix, inspect broad implementation surfaces, or design datasets before happy-path approval. This gate exists to prevent token expenditure on a misunderstood flow without forcing the Product Owner to approve every derived detail.

### 4.6 Complete coverage contract

Registration is incomplete until the owning function or flow documents a coverage matrix that:

- maps every applicable normative PRD requirement, business rule, validation, alternative flow, permission rule, and state transition to at least one executable case;
- considers happy path, negative/validation, boundary/edge, permission/role, state transition, idempotency, concurrency-sensitive, and data-consistency categories;
- marks a category `Not applicable` with a concise reason when it does not apply;
- records any unautomatable or unsafe requirement as an explicit coverage gap requiring human review;
- gives every case deterministic data, observable UI actions, assertions, source references, and a regression tier.

A negative or edge case passes when the system correctly rejects, constrains, or handles the tested condition. Registered cases are not intentionally failing checks.

The function-level command must execute all active cases registered under that function. Case-level selection exists for targeted diagnosis and re-testing, not as the normal completeness path.

## Article 5 — Deterministic Test Data

### 5.1 No AI at runtime

Runtime data creation must use deterministic TypeScript, registered datasets, fixed boundary sets, and seeded pseudo-random generation. It must not call an AI model.

AI may assist humans during dataset design or approved registry maintenance only.

### 5.2 API-assisted prerequisites

Focused function tests should prepare prerequisite state through approved development API calls. The UI action under examination must still be executed and asserted through Playwright.

API preparation must not bypass an action that the selected case claims to test.

### 5.3 Reproducibility

Every execution must record:

- dataset recipe ID and revision;
- runtime seed, where used;
- run ID;
- generated correlation values;
- created backend record identifiers;
- relevant sanitized setup outcomes.

Fresh data must remain reproducible from its recipe, revision, and seed.

### 5.4 Retention and privacy

Generated development data is retained for traceability. It must include a recognizable automation/run marker.

Only synthetic data and dedicated test accounts may be used. Real patient information is prohibited.

Credentials remain under `local-docs/testing-plans/testing-credentials/` or an approved secret store. They must not be copied into registry Markdown, SQLite, screenshots, traces, or logs.

## Article 6 — Execution Contract

### 6.1 Tooling

Normal execution uses Playwright and supporting TypeScript invoked through `pnpm`. Ordinary test runs must not require an AI agent.

### 6.2 Execution levels

The runner must support:

- focused function execution;
- complete module execution;
- selected cross-module flow execution;
- smoke regression;
- affected-scope regression;
- module regression;
- full active-suite regression.

Focused function execution runs every active registered case for that function by default. Selecting one case is an explicit diagnostic or targeted re-test action.

### 6.3 Standard run lifecycle

Every run must:

1. create a unique run ID;
2. validate environment configuration and required accounts;
3. resolve selected active case revisions;
4. check source references and hashes;
5. prepare or locate deterministic synthetic prerequisites;
6. execute Playwright actions and assertions;
7. apply the retry contract;
8. capture evidence according to the final execution outcome;
9. write structured run, attempt, data, artifact, and review records;
10. print the run ID, totals, summary, and pending human-review count.

### 6.4 Synchronization

Tests must use event-based Playwright waits. Fixed delays must not be used as a substitute for observable readiness.

The required delay between failed attempts is retry orchestration, not UI synchronization.

## Article 7 — Retry Contract

Each case receives one initial attempt plus three retries: four attempts maximum.

After each failed attempt except the final attempt, the runner must wait at least five seconds before the next attempt.

Every attempt remains an append-only SQLite record. A later pass or failure must not overwrite an earlier attempt record.

Outcomes are determined as follows:

| Attempt pattern | Preliminary outcome | Review status |
| --- | --- | --- |
| Initial attempt passes | `PASSED` | `REVIEW_NOT_REQUIRED` |
| One or more attempts fail, then a later attempt passes | `FLAKY_OR_TRANSIENT` | `NEEDS_HUMAN_REVIEW` |
| All four attempts fail consistently | `POTENTIAL_ISSUE` | `NEEDS_HUMAN_REVIEW` |
| Attempts fail for materially different reasons | `INCONSISTENT_FAILURE` | `NEEDS_HUMAN_REVIEW` |
| Setup or environment prevents meaningful execution | `BLOCKED` | `NEEDS_HUMAN_REVIEW` |
| Source-reference change is detected | `SOURCE_REVIEW_REQUIRED` | `NEEDS_HUMAN_REVIEW` |
| Deterministic classification is insufficient | `UNKNOWN` | `NEEDS_HUMAN_REVIEW` |

These outcomes are preliminary routing labels, not final diagnoses.

## Article 8 — Evidence Contract

### 8.1 Clean initial pass

- Store structured execution data.
- Do not retain a screenshot.
- Do not retain a Playwright trace.

### 8.2 Consistent failure or potential issue

- Capture a screenshot after each failed attempt to one rolling path.
- Replace the earlier screenshot after each newer failed attempt.
- Retain only the final-attempt screenshot when all attempts fail.
- Retain the final relevant Playwright trace.
- Preserve every attempt and diagnostic record in SQLite.

### 8.3 Flaky or transient execution

- Preserve the most recent failed-attempt screenshot.
- Capture and retain the passing-attempt screenshot.
- Retain the relevant Playwright trace.
- Set `FLAKY_OR_TRANSIENT` and `NEEDS_HUMAN_REVIEW`.

### 8.4 Required diagnostics

Where available and safe, evidence must record:

- failed step and assertion;
- expected and observed values;
- browser and viewport;
- environment and duration;
- attempt number;
- console errors;
- relevant failed network requests;
- API setup diagnostics;
- generated record IDs;
- case, dataset, and source revisions;
- artifact paths and checksums.

Authorization headers, cookies, tokens, passwords, secrets, and sensitive values must be redacted before persistence.

## Article 9 — Result Store and Review Queue

### 9.1 Canonical execution store

SQLite is the canonical execution and review-history store for the initial local/manual model. Large artifacts remain files referenced by path and checksum.

### 9.2 Append-only history

Runs, attempts, result labels, review events, related work items, and re-tests must remain historically queryable. Corrections are recorded as new events rather than destructive replacements.

### 9.3 Serialized writes

Parallel Playwright workers must not perform uncontrolled concurrent SQLite writes. A single reporter/writer or equivalent serialized commit mechanism must own canonical writes.

### 9.4 Human-review visibility

Every non-clean result must receive an explicit `NEEDS_HUMAN_REVIEW` status. The terminal summary and review query must show the pending count so unresolved results cannot disappear into raw logs.

The review queue must support filtering and prioritization by:

- severity or blocker impact;
- module;
- outcome and technical label;
- age;
- run ID;
- case ID;
- review status.

## Article 10 — Human Review

### 10.1 Preliminary technical labels

The deterministic runner may record objective observations such as:

- assertion failed;
- element unavailable;
- navigation failed;
- API setup failed;
- authentication failed;
- network/backend error;
- timeout;
- browser/runner failure;
- source document changed;
- unknown.

These labels must not be presented as confirmed causes.

### 10.2 Review lifecycle

The supported human-review lifecycle is:

```text
NEEDS_HUMAN_REVIEW
  → UNDER_REVIEW
  → BUG_CONFIRMED / TEST_UPDATE_NEEDED / ENVIRONMENT_ISSUE /
    DEFERRED / DUPLICATE / INSUFFICIENT_EVIDENCE /
    NOT_REPRODUCIBLE / CLOSED_NO_CHANGE
  → RETEST_REQUIRED, when applicable
  → VERIFIED or REOPENED
```

### 10.3 Review audit fields

Every human decision must record:

- reviewer identity;
- decision timestamp;
- previous and new status;
- classification and notes;
- related bug, Plane task, fix, or source-change reference;
- whether re-testing is required;
- related re-test execution, when available.

## Article 11 — Frontend and Requirement Changes

### 11.1 No automatic baseline repair

A locator, navigation, label, or layout mismatch must never automatically rewrite a test. It may represent a legitimate UI change, product regression, PRD drift, locator-only change, removed behavior, environment issue, or data issue.

### 11.2 Approved maintenance lifecycle

Test maintenance requires:

1. a result or source change flagged for human review;
2. human or human-triggered AI-assisted investigation;
3. a human decision of `TEST_UPDATE_NEEDED`;
4. an approved registration workflow mode;
5. comparison of live sources, current UI, and current case;
6. a proposed exact change;
7. human approval;
8. targeted validation;
9. a recorded new case revision linked to the originating result.

### 11.3 Reason-specific revisions

Requirement-driven and UI-driven revisions must be distinguished. A legitimate frontend change uses an `update-ui` path. A source-requirement change uses an `update-requirement` path.

No maintenance workflow may edit a PRD merely to make it agree with the frontend.

## Article 12 — AI-Agent Boundaries

### 12.1 Optional, human-triggered assistance

AI may assist only when a human explicitly invokes registration, maintenance, investigation, or drafting work.

### 12.2 Registration responsibility

The proposed `web-e2e-register` skill may support:

- `create`;
- `expand`;
- `update-ui`;
- `update-requirement`;
- `retire`;
- `revalidate`.

It must obtain human approval of the function/flow boundary and canonical happy path, then derive and register the complete applicable PRD-based suite under Articles 1.2, 4.5, and 4.6. It must not require per-case approval for unambiguous derived cases, but it must stop when an Article 1.2 exception applies.

### 12.3 Review responsibility

The proposed `web-e2e-review` skill may load a human-selected pending result, summarize evidence, compare sources and UI behavior, present possible classifications, and record the human's decision.

### 12.4 Prohibited autonomous actions

No AI agent may:

- invent an expected behavior that is not directly grounded in an approved source;
- resolve conflicting or ambiguous product intent without human direction;
- change locators, steps, datasets, or assertions of an existing approved case outside the maintenance lifecycle in Article 11;
- change an approved expected outcome;
- approve a discrepancy;
- confirm a bug;
- suppress, discard, or close a result;
- retire a case;
- create an external task.

## Article 13 — Repository and Retention Rules

### 13.1 Version-controlled assets

The following should be version-controlled when implemented:

- this constitution and architecture;
- registry Markdown and approved executable cases;
- framework source;
- database schema and migrations;
- deterministic dataset definitions;
- non-secret configuration examples.

### 13.2 Generated assets

The growing SQLite database, screenshots, traces, downloads, and runtime logs should normally be excluded from Git and backed up separately according to an approved retention policy.

### 13.3 No destructive cleanup by default

Generated backend records and historical result records must not be automatically deleted. Any later cleanup policy requires explicit approval and must preserve required traceability.

## Article 14 — Amendment and Approval

### 14.1 Amendment record

Every approved amendment must record:

- constitution version;
- date;
- changed articles;
- reason;
- approving human;
- related architecture or implementation decision.

### 14.2 Approval state

Version `1.2` is the approved governing baseline. Testing evidence may justify later amendments, but test runs and AI recommendations cannot change this document automatically.

### 14.3 Next gate

After constitution approval, the next implementation gate is to define:

1. stable identifier syntax and the registered-case Markdown template;
2. the SQLite schema and migration contract;
3. the minimal deterministic runner/reporter interface;
4. the first Provider pilot module.

Runtime code must follow test-driven development from its first behavior.

## Amendment Log

| Version | Date | Status | Summary | Approved by |
| --- | --- | --- | --- | --- |
| 0.1-draft | 2026-07-11 | Superseded | Initial constitution derived from the approved E2E architecture | Pending at creation |
| 1.0 | 2026-07-11 | Approved | Initial governance baseline approved for iterative improvement through testing evidence | Product Owner |
| 1.1 | 2026-07-12 | Approved | Added the PRD flow scout and mandatory Product Owner flow-approval gate before detailed registration | Product Owner |
| 1.2 | 2026-07-15 | Approved | Changed registration approval from per-case review to happy-path approval plus delegated, requirement-complete PRD-derived suite registration; preserved mandatory human issue decisions | Product Owner |
