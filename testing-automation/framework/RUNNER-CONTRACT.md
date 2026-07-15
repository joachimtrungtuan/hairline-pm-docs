# Deterministic Runner and Reporter Contract

**Status:** Function runner, interactive registry selector, and review queue implemented; dedicated module/flow/regression commands remain pending
**Governed by:** `local-docs/testing-automation/TESTING-CONSTITUTION.md`

## 1. Boundary

The runner executes approved registered cases without AI. The reporter serializes results, manages constitutional evidence, and exposes the human-review queue. Neither component makes final product decisions.

## 2. Command Interface

### 2.1 Initial development environment profile

| Setting | Value |
| --- | --- |
| Dashboard base URL | `https://admin.hairline.app` |
| Provider login | `/auth/provider/login` |
| Admin login | `/auth/hairline-team/login` |
| Credential references | `local-docs/testing-plans/testing-credentials/` |

Provider and Admin use the same dashboard origin. Credentials must be resolved securely and must never be copied into runtime results or terminal output.

### 2.2 Commands

The initial interface is:

```bash
./test.sh
pnpm test:function <module-id> <function-id> [--case <case-id>]
pnpm test:module <module-id>
pnpm test:flow <flow-id>
pnpm test:regression smoke
pnpm test:regression affected <module-or-requirement-id>
pnpm test:regression module <module-id>
pnpm test:regression full
pnpm test:review-queue [filters]
```

`./test.sh` is the primary human interface. It reads active module/function/flow metadata from the same TypeScript registry used by the runner, runs preflight before browser execution, and delegates to the deterministic pnpm commands. It must not duplicate case definitions, expose draft execution, or change runner outcomes and review rules.

Every command must support a help mode and return a non-zero exit code for invalid selection, environment failure, writer failure, or any result requiring human review. Exact exit-code numbers will be specified with failing contract tests before implementation.

## 3. Runner Phases

```text
preflight
  → selection
  → source check
  → deterministic data setup
  → Playwright execution
  → bounded retry orchestration
  → evidence finalization
  → recovery envelope
  → serialized SQLite commit
  → terminal summary
```

### 3.1 Preflight

Validate:

- development environment configuration;
- base URL reachability;
- required account references without printing secrets;
- writable result and artifact locations;
- compatible SQLite schema version;
- unique run ID allocation.

### 3.2 Selection

Resolve only approved `ACTIVE` case revisions by default. Review-required cases may run against their last approved revision but must be surfaced in the review queue.

The runner must reject duplicate case IDs, unknown modules, invalid flow ownership, and missing automation mappings.

### 3.3 Source check

Compare approved and observed normalized source hashes. Never copy source text into the runtime result database.

### 3.4 Data setup

Execute registered TypeScript dataset recipes with a recorded seed. API calls prepare prerequisites but may not bypass the action claimed by the selected case.

### 3.5 Execution and retry

- Run one initial attempt.
- After failure, wait at least five seconds.
- Run up to three retries.
- Stop immediately after a passing attempt.
- Preserve every attempt record.
- Treat recovered execution as `FLAKY_OR_TRANSIENT`, never a clean pass.

### 3.6 Evidence finalization

- Clean initial pass: retain no screenshot or trace.
- All attempts fail: overwrite the rolling screenshot after each failure; retain the final screenshot and relevant trace.
- Later attempt passes: retain the most recent failed screenshot, passing screenshot, and relevant trace.
- Record checksums and safe relative paths.

## 4. Worker Result Envelope

Workers must emit a validated, versioned JSON envelope containing:

- schema version;
- run and execution IDs;
- case/function/flow/module identity;
- case and dataset revisions;
- source hash results;
- attempt observations;
- preliminary labels and outcome;
- sanitized setup and error summaries;
- generated record references;
- artifact metadata;
- payload checksum.

The envelope contains no final human classification and no secrets. It is a recovery buffer, not the canonical query store.

## 5. Reporter Responsibilities

The single reporter/writer must:

1. validate envelope version and checksum;
2. redact again at the persistence boundary;
3. verify referenced artifact paths and checksums;
4. commit the case execution atomically;
5. create `NEEDS_HUMAN_REVIEW` where constitutionally required;
6. preserve idempotency during envelope replay;
7. close the run with derived totals;
8. print a concise terminal summary.

## 6. Terminal Summary

The summary must include:

- run ID and command;
- selected environment;
- passed, flaky, potential issue, blocked, inconsistent, source-review, and unknown counts;
- newly created human-review items;
- total pending human-review count;
- result database path;
- artifact root when artifacts exist;
- command to inspect the review queue.

It must not print credentials, tokens, cookies, or raw sensitive payloads.

## 7. Review Queue Interface

`pnpm test:review-queue` must be deterministic and read-only. Initial filters should support:

- review status;
- module;
- priority/blocker impact;
- preliminary outcome;
- age range;
- run ID;
- case ID;
- limit and sort order.

Changing a review status is outside the ordinary runner. It requires a human-controlled review command or the human-triggered review skill after its design is approved.

## 8. Failure Boundaries

| Failure point | Required behavior |
| --- | --- |
| Preflight fails | Record/print environment failure where storage is available; do not start cases |
| Dataset setup fails | Mark case `BLOCKED`; apply review requirement; do not claim UI failure |
| Browser action/assertion fails | Apply retry and evidence policy |
| Artifact write fails | Preserve execution result, label evidence failure, require human review |
| Recovery envelope write fails | Stop before claiming result persistence |
| SQLite commit fails | Keep envelope for replay; exit non-zero |
| Terminal rendering fails after commit | Do not replay committed execution; allow summary regeneration |

## 9. TDD Implementation Order

Runtime implementation must begin with failing tests in this order:

1. identifier and registry selection validation;
2. retry count and minimum-delay orchestration using an injected clock;
3. preliminary outcome derivation;
4. screenshot/trace retention decisions;
5. envelope validation and redaction;
6. idempotent serialized SQLite writes;
7. review-status creation;
8. terminal summary and exit behavior;
9. Playwright integration;
10. first registered case.

No runner, reporter, or database writer production code should precede its failing contract test.

## 10. Deferred Decisions

- Exact exit-code numbers.
- Package layout and TypeScript build mode.
- Playwright version and browser baseline.
- SQLite library.
- Default viewport matrix.
- Pilot Provider module.
