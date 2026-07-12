# Hairline Web E2E Testing Architecture

**Document type:** Testing architecture and operating contract
**Status:** Approved design; constitution v1.1 approved; SQLite/review foundation integration-tested
**Date:** 2026-07-11
**Initial scope:** Provider Dashboard and Admin Dashboard in the development environment
**Primary tools:** Playwright, TypeScript, pnpm, SQLite

---

## 1. Purpose

This document defines a long-term, repeatable web end-to-end testing system for Hairline. The system must reduce repetitive manual testing while preserving human control over product judgments, test-case changes, and confirmed bug decisions.

The design supports:

- focused testing of individual functions;
- complete testing of a module's internal flows;
- cross-module business-flow testing;
- fresh synthetic datasets for happy, negative, boundary, permission, and state-transition scenarios;
- deterministic command-line execution without AI-agent involvement;
- relational execution history for later retrieval and analysis;
- regression testing after bug fixes, blocker removal, requirement changes, or frontend changes;
- evidence detailed enough to support later human review and optional AI-assisted investigation.

This document defines the architecture. The constitution, contracts, reusable framework, registration/review skills, and contract-tested result foundation exist beside it. The product registry and canonical result database are intentionally empty until the first approved registration.

## 2. Design Principles

### 2.1 Human authority

Every non-passing or recovered-after-retry result requires human review. Neither the deterministic runner nor an AI agent may make a final product judgment.

Only a human reviewer may:

- confirm a bug;
- approve a test-case change;
- approve a changed expected result;
- accept an implementation discrepancy;
- retire or supersede a test case;
- close or defer a review item.

### 2.2 Source authority without duplication

The testing system must refer to the live source documents under `local-docs/`; it must not rewrite or copy their requirements into the test registry.

Applicable sources may include:

- `local-docs/project-requirements/system-prd.md`;
- the relevant functional PRD under `local-docs/project-requirements/functional-requirements/`;
- the relevant product plan under `local-docs/product-plans/`.

Registered cases store source paths, requirement identifiers, and headings. They contain only the test-specific interpretation needed to execute and evaluate a case.

Live development APIs may be inspected as implementation evidence and used for deterministic test-data preparation. They do not automatically override PRD-defined expected behavior.

### 2.3 Module-first traceability

The existing Hairline module list is the primary classification system. Every function, case, dataset, flow, result, review, and artifact must be traceable to a primary module.

A cross-module flow has one primary owning module and records all participating modules as relationships. The same flow must not be duplicated under every participating module.

### 2.4 Deterministic execution

Normal execution must be ordinary Playwright and supporting TypeScript code invoked with `pnpm`. It must not require an AI agent or consume agentic tokens.

### 2.5 Evidence proportionality

Clean passes retain structured result data but no screenshots or Playwright traces. Potential issues and flaky cases retain the evidence defined in Section 10.

### 2.6 Append-only history

Test executions and human-review decisions form historical evidence. Later retries, re-tests, or case revisions must not overwrite earlier database records.

## 3. Scope and Non-Goals

### 3.1 Initial scope

- Provider Dashboard web functions and flows.
- Admin Dashboard web functions and flows.
- Development environment only, using the shared dashboard base URL `https://admin.hairline.app`.
- Provider login route: `/auth/provider/login`.
- Admin login route: `/auth/hairline-team/login`.
- API-assisted preparation of synthetic prerequisite data.
- Browser-level verification against the real development frontend and backend.

### 3.2 Future-compatible scope

The architecture may later support additional tenants, environments, browsers, viewports, or CI execution. Those additions must not weaken the human-review gate.

### 3.3 Non-goals

- Mobile-app automation is not part of the initial web E2E system.
- This system is not a load- or stress-testing tool.
- It does not replace backend unit or API contract tests.
- It does not automatically rewrite tests when the frontend changes.
- It does not automatically confirm or create bug reports.
- It does not copy PRD content into a parallel testing specification.
- It does not clean up generated development data by default.

## 4. Proposed Top-Level Structure

The implementation should use the permanent `local-docs/testing-automation/` area with the following conceptual structure:

```text
testing-automation/
├── TESTING-CONSTITUTION.md
├── registry/
├── framework/
├── pilot-plans/
└── results/
```

### 4.1 `TESTING-CONSTITUTION.md`

The constitution is the governing contract for registration, execution, evidence, review, maintenance, and traceability. At minimum, it must define:

- source-of-truth order;
- stable identifier rules;
- test and dataset classifications;
- execution and retry policy;
- result and review statuses;
- API-assisted data-creation rules;
- evidence retention;
- credential and sensitive-data handling;
- AI-agent boundaries;
- test-case revision and retirement rules;
- regression tiers.

### 4.2 `registry/`

The registry contains human-reviewed test definitions and their executable module-local assets. It is organized by tenant, module, and then function or flow.

```text
registry/
├── provider/
│   └── PR-XX-<module-name>/
│       ├── module.md
│       ├── functions/
│       │   └── <function-id>-<function-name>/
│       │       ├── test-cases.md
│       │       ├── datasets.ts
│       │       └── tests.spec.ts
│       └── flows/
│           └── <flow-id>-<flow-name>/
│               ├── test-cases.md
│               ├── datasets.ts
│               └── flow.spec.ts
└── admin/
    └── A-XX-<module-name>/
        └── ...
```

The initial registry contract uses one `test-cases.md` collection per function or flow, with separate TypeScript datasets and specs. `registry/IDENTIFIERS.md` and `registry/CASE-TEMPLATE.md` define the initial stable ID and Markdown contracts. The module-first classification and stable IDs are mandatory.

### 4.3 `framework/`

The framework contains reusable execution machinery, not copied requirements or module-specific business rules.

```text
framework/
├── api/             # Reusable authenticated development API clients
├── authentication/  # Account/session preparation
├── data-builders/   # Deterministic synthetic-data builders
├── fixtures/        # Playwright fixtures
├── pages/           # Genuinely reusable UI interaction helpers
├── reporters/       # SQLite writer and terminal summaries
└── runtime/         # Configuration, run IDs, paths, environment checks
```

A helper begins inside its owning module. It moves into `framework/` only after genuine reuse across multiple modules is demonstrated.

### 4.4 `results/`

```text
results/
├── test-results.sqlite
└── artifacts/
    ├── provider/
    │   └── PR-XX-<module-name>/
    │       └── <run-id>/
    │           └── <case-id>/
    └── admin/
        └── A-XX-<module-name>/
            └── <run-id>/
                └── <case-id>/
```

SQLite stores structured history and artifact metadata. Screenshots, traces, downloads, and large logs remain filesystem artifacts referenced by path from SQLite.

The growing SQLite database and runtime artifacts should normally be excluded from Git. The registry, constitution, framework source, migrations, and database schema definitions should be version-controlled. A backup policy for retained history must be defined before production use of the testing system.

### 4.5 `pilot-plans/`

Pilot plans contain discovery evidence and proposed registry allocations before cases become active. They preserve the review boundary between investigation and registration. An approved proposal is translated into the module-first `registry/`; the proposal remains as decision history.

## 5. Registered Test-Case Contract

Each registered test case must include or resolve the following metadata:

| Field | Purpose |
| --- | --- |
| Case ID | Stable identifier that remains unchanged across revisions |
| Title | Concise behavior under test |
| Primary module | Owning Hairline module |
| Participating modules | Other modules involved, if any |
| Function or flow ID | Stable registry grouping |
| Test level | Function, module flow, or cross-module flow |
| Scenario category | Happy, negative, boundary, permission, state transition, or other approved category |
| Priority / regression tier | Smoke, affected, module, or full-suite relevance |
| Source references | Live paths plus requirement IDs and headings |
| Preconditions | Required system state expressed as testing intent |
| Data recipe | Deterministic API-assisted dataset definition |
| UI actions | Current approved interaction mapping |
| Assertions | Observable outcomes to verify |
| Automation reference | Playwright spec and test name |
| Registry status | Active, review required, superseded, retired, or other approved state |
| Last UI-confirmed date | Most recent human-confirmed implementation mapping |
| Revision | Monotonic case-definition revision |

The registry must not restate whole requirements. A concise assertion may describe an observable expected outcome, but the authoritative business rule remains in its source document.

### 5.1 Source-change detection

Each registered case should store a hash for the exact source sections or requirement blocks used at its most recent approval. The execution record stores the case revision and hashes used for that run.

When a source hash changes:

- the case is labelled `SOURCE_REVIEW_REQUIRED`;
- execution may continue against the currently approved case definition;
- the result enters the human-review queue even if functional assertions pass;
- no expected outcome is changed automatically.

The pilot must validate a stable section-hashing approach that does not treat unrelated line movement or formatting-only edits as requirement changes.

## 6. Test Data Strategy

### 6.1 API-assisted prerequisite creation

Focused function tests should create their prerequisite records through deterministic development API calls. The UI action under examination remains a real browser interaction against the real development frontend and backend.

Example: a provider check-in test may create or advance a synthetic booking to the required fully-paid state through approved API helpers, then perform and verify check-in through the Provider Dashboard UI.

### 6.2 Whole-flow behavior

Module and cross-module flows may exercise a longer sequence of real UI actions where the earlier steps are part of the behavior under test. API creation must not bypass an action that the selected case claims to verify.

### 6.3 Deterministic variation

Runtime data generation may vary values without AI by using registered recipes, seeded pseudo-random generation, and explicit boundary sets. Every execution must record:

- data recipe ID and revision;
- random seed, when used;
- unique run ID;
- generated identifiers and correlation values;
- created backend record IDs;
- relevant setup responses or sanitized summaries.

This makes every supposedly fresh dataset reproducible.

### 6.4 Retention

Generated development data is retained. It must carry a recognizable automation/run identifier so later investigation can correlate UI evidence, backend records, and SQLite history.

Retention does not permit real patient information. Only dedicated test accounts and synthetic data may be used.

## 7. Execution Levels and Commands

All commands use `pnpm`.

### 7.1 Function

Runs one function or a selected case with API-created prerequisites.

```bash
pnpm test:function PR-XX <function-id>
```

### 7.2 Module

Runs all active registered functions in one module, followed by its internal module flows.

```bash
pnpm test:module PR-XX
```

### 7.3 Cross-module flow

Runs one registered business journey involving its primary and participating modules.

```bash
pnpm test:flow <flow-id>
```

### 7.4 Regression

```bash
pnpm test:regression smoke
pnpm test:regression affected PR-XX
pnpm test:regression module PR-XX
pnpm test:regression full
```

Regression tiers mean:

- `smoke`: critical availability and primary journeys;
- `affected`: cases mapped to the selected module, function, flow, or requirement;
- `module`: all active cases owned by one module;
- `full`: all active automated cases.

The final command names are an interface contract to validate during implementation; their underlying script composition may vary.

### 7.5 Standard execution lifecycle

Every command must:

1. Create a unique run ID.
2. Validate environment configuration and required test accounts.
3. Resolve selected registry cases and their current revisions.
4. Check source hashes.
5. Create or locate synthetic prerequisites through deterministic APIs.
6. Execute Playwright assertions.
7. Apply the retry policy.
8. Capture evidence according to the final result.
9. Write run, attempt, data, artifact, and review-queue records to SQLite.
10. Print the run ID, totals, result summary, and pending human-review count.

## 8. Retry Policy

Each selected case has one initial attempt and three retries: four attempts maximum.

```text
Attempt 1
  wait at least 5 seconds after failure
Attempt 2
  wait at least 5 seconds after failure
Attempt 3
  wait at least 5 seconds after failure
Attempt 4
```

All attempts are stored in SQLite. A later attempt never erases the historical result of an earlier attempt.

The default five-second separation is a minimum, not a fixed wait strategy inside the test. Tests must still use event-based Playwright waits rather than arbitrary sleep calls for normal UI synchronization.

## 9. Execution Outcomes and Human-Review Statuses

Execution outcome and review status are separate fields.

### 9.1 Preliminary execution outcomes

| Outcome | Meaning |
| --- | --- |
| `PASSED` | Initial attempt passed |
| `FLAKY_OR_TRANSIENT` | One or more attempts failed and a later attempt passed |
| `POTENTIAL_ISSUE` | All four attempts failed consistently |
| `INCONSISTENT_FAILURE` | Attempts failed for materially different reasons |
| `BLOCKED` | Setup, authentication, environment, or required prerequisite prevented execution |
| `SOURCE_REVIEW_REQUIRED` | A referenced source section changed since case approval |
| `UNKNOWN` | Deterministic classification is insufficient |

These labels are routing information only. They do not determine whether the product, environment, source document, or test is wrong.

### 9.2 Preliminary technical labels

The runner may attach objective labels such as:

- assertion failed;
- element unavailable;
- navigation failed;
- API data setup failed;
- authentication failed;
- network/backend error;
- timeout;
- browser/runner failure;
- source document changed;
- unknown.

### 9.3 Review lifecycle

Every outcome other than a clean `PASSED` result receives `NEEDS_HUMAN_REVIEW`.

```text
NEEDS_HUMAN_REVIEW
        ↓
UNDER_REVIEW
        ↓
BUG_CONFIRMED / TEST_UPDATE_NEEDED / ENVIRONMENT_ISSUE /
DEFERRED / DUPLICATE / INSUFFICIENT_EVIDENCE /
NOT_REPRODUCIBLE / CLOSED_NO_CHANGE
        ↓
RETEST_REQUIRED, when applicable
        ↓
VERIFIED or REOPENED
```

Only a human reviewer may apply a final review classification. Each review action must record reviewer, timestamp, decision, notes, related bug/task identifiers, and re-test requirement.

The default review queue must clearly expose pending counts and support prioritization by severity, blocker impact, module, age, and run.

## 10. Evidence Policy

### 10.1 Clean pass

- Store structured result and timing data in SQLite.
- Do not retain a screenshot.
- Do not retain a Playwright trace.

### 10.2 Consistent or potential issue

- Capture a screenshot after every failed attempt to the same rolling path.
- Each later failure replaces the previous screenshot.
- After the final failure, retain only the final-attempt screenshot.
- Retain the final relevant Playwright trace.
- Preserve all attempt records and technical diagnostics in SQLite.

### 10.3 Flaky or transient case

- Preserve the most recent failed-attempt screenshot.
- Capture and preserve the later passing-attempt screenshot.
- Retain the relevant Playwright trace.
- Mark the execution `FLAKY_OR_TRANSIENT` and `NEEDS_HUMAN_REVIEW`.

### 10.4 Additional diagnostics

Where available, SQLite or referenced artifacts should retain:

- failed step and assertion;
- expected and observed values;
- browser, viewport, environment, and duration;
- console errors;
- failed or relevant network requests;
- retry/attempt number;
- API setup diagnostics;
- generated record IDs;
- source and case revisions.

Credentials, tokens, secrets, and sensitive values must be redacted before persistence.

## 11. SQLite Result Store

SQLite is the recommended canonical result store for the current single-project, primarily local/manual execution model.

It provides relational queries, transactional writes, portability, simple backup, and direct Node.js integration without requiring a database server.

### 11.1 Conceptual entities

The schema should include at least:

- `test_runs` — one record per command invocation;
- `case_definitions` — snapshots of registered case identity/revision metadata;
- `case_executions` — one selected case within a run;
- `attempts` — initial attempt and retries;
- `execution_labels` — objective preliminary labels;
- `source_references` — referenced paths, requirement IDs, headings, and hashes;
- `datasets` — recipe and runtime seed metadata;
- `generated_records` — retained backend record identifiers and correlations;
- `artifacts` — type, path, attempt, checksum, and retention metadata;
- `human_reviews` — reviewer decisions and notes;
- `review_events` — append-only review-status transitions;
- `related_items` — bug IDs, Plane keys, fix references, or re-test links;
- `module_relationships` — primary and participating module mappings.

### 11.2 Concurrency

Playwright workers should not perform uncontrolled concurrent writes to SQLite. The implementation should use a single reporter/writer process or another serialized commit mechanism. Worker results may be buffered as structured payloads before the canonical writer commits them.

### 11.3 Schema lifecycle

- Schema migrations must be version-controlled.
- Runtime startup must verify schema compatibility.
- Migrations must preserve historical result and review records.
- Direct manual edits to the result database should be avoided in favor of controlled commands.

SQLite should be reconsidered only if Hairline later requires centralized multi-machine execution with sustained concurrent writers or shared remote review. PostgreSQL would then be the likely migration target. DuckDB may complement analytics but should not replace the canonical transactional store in the initial design.

## 12. Frontend and Requirement Change Handling

A failed locator or changed navigation does not automatically mean the test is outdated. Human review must determine whether:

- the frontend changed legitimately and the registered UI mapping needs revision;
- the frontend drifted from the PRD;
- the PRD changed and the test requires requirement-driven revision;
- behavior is unchanged and only a locator changed;
- the feature was removed or altered accidentally;
- the environment or data setup caused the discrepancy.

Approved test maintenance follows this lifecycle:

```text
Non-pass or source-change result
        ↓
NEEDS_HUMAN_REVIEW
        ↓
Human or human-triggered AI-assisted investigation
        ↓
Human decision: TEST_UPDATE_NEEDED
        ↓
Invoke the registration skill in the appropriate update mode
        ↓
Compare live source documents, current UI, and existing case
        ↓
Propose exact registry and script changes
        ↓
Human approval
        ↓
Apply, validate, record revision, and link the originating result
```

No maintenance workflow may rewrite the source PRD merely to match the frontend.

## 13. AI-Agent Boundaries and Proposed Skills

AI is optional and human-triggered. Normal Playwright execution, retrying, evidence capture, result recording, and queue creation must remain deterministic and token-free.

### 13.1 Proposed `web-e2e-register`

This skill owns approved creation and maintenance of registered cases. Proposed modes:

- `create`;
- `expand`;
- `update-ui`;
- `update-requirement`;
- `retire`;
- `revalidate`.

Its responsibilities include:

- locating source documents through `local-docs/INDEX.md`;
- first reading only the PRD module scope and overall business workflows;
- returning a concise flow outline and stopping for Product Owner corrections and approval;
- beginning detailed UI/API/dataset/case discovery only after that flow approval;
- inspecting the implemented dashboard UI;
- inspecting relevant APIs for deterministic setup;
- proposing case and dataset coverage;
- waiting for human approval before changes;
- creating or updating registry Markdown, datasets, and Playwright scripts;
- recording source references and case revisions;
- running targeted validation after approved changes.

### 13.2 Proposed `web-e2e-review`

This skill supports a human-selected review item. It may:

- query pending SQLite review records;
- load the selected attempts, diagnostics, screenshots, and trace;
- compare evidence with the registered case and live source documents;
- inspect the current UI or implementation when authorized;
- explain likely causes and present human decision options;
- record the human's chosen review status;
- draft a bug report or test update when explicitly requested.

### 13.3 Prohibited AI actions

No AI agent may automatically:

- change locators, steps, datasets, or assertions;
- change expected outcomes;
- approve a frontend discrepancy;
- mark a result `BUG_CONFIRMED`;
- discard or suppress a result;
- retire a case;
- create an external task without approval.

## 14. Security, Privacy, Reliability, and Maintenance

### 14.1 Security and privacy

- Use only dedicated test accounts from `local-docs/testing-plans/testing-credentials/`.
- Keep credentials outside test-case Markdown and SQLite result content.
- Redact authorization headers, cookies, tokens, passwords, and sensitive payload fields.
- Use synthetic data; never use real patient information.

### 14.2 Reliability

- Prefer accessible roles, stable labels, and approved test IDs over fragile CSS selectors.
- Use event-based waits instead of arbitrary in-test delays.
- Treat the five-second retry separation as retry orchestration, not UI synchronization.
- Record sufficient setup and network evidence to distinguish product behavior from environment failure.
- Preserve the original failure even if a retry passes.

### 14.3 Performance expectations

Function tests should remain focused and use API-assisted setup. Smoke coverage should remain intentionally small. Full-suite duration must be measured during the pilot before hard service-level targets are adopted.

### 14.4 Ownership

The test registry and Playwright implementation are maintained product assets. Requirement changes, approved frontend changes, and relevant bug fixes must include an explicit assessment of affected tests.

## 15. Pilot and Rollout Sequence

Implementation should proceed in controlled stages:

1. Approve this architecture.
2. Create and approve `TESTING-CONSTITUTION.md`.
3. Define stable IDs and the Markdown case template.
4. Define and review the SQLite schema and migrations.
5. Create the minimal deterministic runner and reporter.
6. Select one Provider module as the pilot.
7. Register its source-linked functions, flows, and datasets.
8. Validate API-assisted setup against the development environment.
9. Validate retries, screenshots, traces, SQLite writes, and the review queue.
10. Perform human review of pilot outputs.
11. Revise the architecture only where pilot evidence requires it.
12. Create the two agent skills after the underlying contracts are proven.
13. Expand module by module, then add cross-module regression flows.

The pilot module should be important enough to exercise meaningful state transitions, but contained enough that its prerequisites and UI can be understood without first automating the entire platform.

## 16. Risks and Mitigations

| Risk | Mitigation |
| --- | --- |
| Frontend drift creates fragile tests | Human-reviewed UI mappings, stable locators, explicit `update-ui` workflow |
| PRD updates silently stale cases | Section-level hashes and `SOURCE_REVIEW_REQUIRED` queue status |
| Retry hides intermittent failures | Preserve attempt history; recovered cases remain human-review items |
| Large evidence volume | No artifacts for clean passes; rolling failure screenshot; module/run organization |
| SQLite write locks under parallelism | Single serialized result writer |
| Generated data becomes untraceable | Run IDs, seeds, recipe revisions, and backend record IDs |
| AI changes the baseline incorrectly | Human-triggered skills and mandatory approval gates |
| Copied requirements diverge | References only; no parallel PRD text |
| Environment failures appear to be product bugs | Preliminary technical labels plus human classification |
| Review queue grows unnoticed | Explicit review status, pending count, priority/age queries, terminal summary |

## 17. Decision Log

| Decision | Alternatives considered | Reason |
| --- | --- | --- |
| Use Playwright as a deterministic CLI runner | Agent-driven browser execution | Repeatable execution without token consumption |
| Use `pnpm` for all commands | npm | Project preference and one package-manager contract |
| Use API-assisted prerequisite setup | Entirely UI-created setup | Faster isolated function tests with fewer unrelated blockers |
| Retain generated development data | Automatic cleanup | Enables later correlation and investigation |
| Use Markdown for the registry | SQLite-only definitions | Human reviewability and source control |
| Use SQLite for results | Markdown, CSV, JSONL, DuckDB, PostgreSQL | Relational queries and portability without a server |
| Store large artifacts as files | SQLite BLOBs | Keeps the database manageable and artifacts directly inspectable |
| Organize primarily by module | Requirement-only or tenant-only hierarchy | Matches Hairline's established classification and product plans |
| Give cross-module flows one owner | Duplicate flows under each module | Avoids divergent copies while preserving relationships |
| Reference PRDs without copying them | Duplicate testing requirements | Prevents source discrepancies after PRD changes |
| Use one initial attempt plus three retries | No retry or indefinite retry | Detects transient behavior while keeping bounded execution |
| Wait at least five seconds between failed attempts | Immediate retry | Provides a consistent recovery window |
| Require human review for every non-pass | Automated AI or runner decisions | Preserves human product authority |
| Keep final screenshot for consistent failures | Retain every failed screenshot | Controls artifact growth while preserving final state |
| Keep failed and passing screenshots for flaky cases | Final screenshot only | Provides before/after evidence for intermittent behavior |
| Retain traces for potential issues and flaky cases only | Trace every run | Useful diagnostics without pass-run storage growth |
| Separate registration and review skills | One combined skill | Clear authority and narrower workflows |
| Let `web-e2e-register` maintain approved UI changes | Manual unstructured edits | Traceable, source-aware test maintenance |
| Reuse global Playwright MCP and system Chrome | Project-local Playwright dependency | Avoids duplicate installation and keeps the test workspace independent from application source |
| Prohibit runtime or documentation dependency on `main/` | Read-only source mapping | Keeps automation based on PRDs, live UI, and live API behavior only |

## 18. Open Implementation Questions

The following questions remain deferred to the pilot or runtime design:

- Section-hashing method that ignores irrelevant formatting changes.
- Result database backup location and retention schedule.
- Default browser and viewport matrix beyond the initial desktop baseline.

These choices must be documented before or during the pilot and added to the constitution or implementation specification as appropriate.

## 19. Approval and Next Gate

This architecture captures the approved design and its evidence-driven amendments. `TESTING-CONSTITUTION.md` version 1.1 is the active baseline. The runtime foundation now covers IDs, retries/outcomes, evidence decisions, envelopes, redaction, transactional/idempotent SQLite writes, review queues, and summaries through TDD; Playwright and live API mutation remain pending.

The MVP framework is implemented without a project Playwright installation. Pilot records and controlled proof data were removed after validating the mechanism. The next gate is a clean `web-e2e-register` run for the first Product Owner-approved flow.
