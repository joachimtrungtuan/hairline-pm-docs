# SQLite Result Schema Contract

**Status:** MVP schema implemented with Node built-in SQLite; canonical runtime database starts with the first registered test
**Canonical database:** `local-docs/testing-automation/results/test-results.sqlite`
**Governed by:** `local-docs/testing-automation/TESTING-CONSTITUTION.md`

## 1. Scope

This document defines the relational contract. The first tested implementation uses Node's built-in `node:sqlite` `DatabaseSync` and an internal migration function for the initial run, execution, attempt, and review-event subset. It does not create the canonical database until the runner is connected.

The result store separates immutable execution observations from append-only human-review events.

## 2. Core Relationships

```text
test_runs
  └── case_executions
       ├── attempts
       │    ├── execution_labels
       │    └── artifacts
       ├── case_source_snapshots
       ├── execution_datasets
       │    └── generated_records
       ├── module_relationships
       ├── review_events
       └── related_items
```

## 3. Table Contracts

### 3.1 `schema_migrations`

| Column | Contract |
| --- | --- |
| `version` | Primary key; monotonic migration identifier |
| `applied_at` | UTC timestamp |
| `checksum` | Migration-content checksum |

### 3.2 `test_runs`

| Column | Contract |
| --- | --- |
| `id` | Human-readable run ID; primary key |
| `command` | Normalized pnpm command/interface invoked |
| `selection_type` | Function, module, flow, smoke, affected, or full |
| `selection_value` | Selected identifier, if applicable |
| `environment` | Development environment identifier |
| `base_url` | Sanitized tested frontend URL |
| `started_at`, `finished_at` | UTC timestamps |
| `status` | Running, completed, interrupted, or writer-failed |
| `browser`, `browser_version` | Runtime browser metadata |
| `viewport_json` | Validated viewport payload |
| `runner_version` | Testing framework version/commit |
| `pending_review_count` | Derived-at-close summary, not review authority |

### 3.3 `case_executions`

| Column | Contract |
| --- | --- |
| `id` | UUID primary key |
| `run_id` | Foreign key to `test_runs` |
| `case_id` | Stable registry case ID |
| `case_revision` | Exact approved revision executed |
| `function_or_flow_id` | Stable owning function/flow ID |
| `primary_module_id` | Primary Hairline module |
| `title_snapshot` | Case title at execution time |
| `registry_status_snapshot` | Registry state at selection time |
| `preliminary_outcome` | Constitutional execution outcome |
| `review_status` | Current review-queue status |
| `started_at`, `finished_at` | UTC timestamps |
| `duration_ms` | Whole case duration including retries |
| `final_attempt_number` | Last attempt executed |
| `writer_payload_checksum` | Recovery/audit checksum |

Unique contract: one case revision may execute once per run unless an explicitly identified re-test execution is created.

### 3.4 `attempts`

| Column | Contract |
| --- | --- |
| `id` | UUID primary key |
| `case_execution_id` | Foreign key |
| `attempt_number` | Integer 1-4 |
| `status` | Passed, failed, blocked, or interrupted |
| `started_at`, `finished_at`, `duration_ms` | Timing |
| `failed_step` | Sanitized step description |
| `expected_summary`, `observed_summary` | Sanitized diagnostic summaries |
| `error_name`, `error_message`, `stack_summary` | Sanitized error data |
| `console_error_count`, `failed_request_count` | Diagnostic counts |

Unique contract: `(case_execution_id, attempt_number)`.

### 3.5 `execution_labels`

| Column | Contract |
| --- | --- |
| `id` | UUID primary key |
| `attempt_id` | Foreign key |
| `label` | Objective preliminary technical label |
| `detail` | Sanitized supporting observation |

Labels are never confirmed causes.

### 3.6 `case_source_snapshots`

| Column | Contract |
| --- | --- |
| `id` | UUID primary key |
| `case_execution_id` | Foreign key |
| `source_reference_id` | Stable registry source-reference ID |
| `source_path` | Live relative path used |
| `requirement_or_heading` | Requirement ID or heading |
| `approved_hash` | Hash stored by approved case revision |
| `observed_hash` | Hash observed before execution |
| `hash_status` | Match, changed, unavailable, or error |

The source text itself is not copied into SQLite.

### 3.7 `execution_datasets`

| Column | Contract |
| --- | --- |
| `id` | UUID primary key |
| `case_execution_id` | Foreign key |
| `dataset_id`, `dataset_revision` | Registered recipe identity |
| `seed` | Reproduction seed, if applicable |
| `setup_status` | Pending, passed, failed, or partial |
| `sanitized_setup_summary` | Non-secret setup result |

### 3.8 `generated_records`

| Column | Contract |
| --- | --- |
| `id` | UUID primary key |
| `execution_dataset_id` | Foreign key |
| `record_type` | Domain record type |
| `backend_record_id` | Backend identifier as text |
| `correlation_key` | Automation/run marker |
| `sanitized_metadata_json` | Validated non-secret metadata |

Generated records are retained; this table does not imply deletion ownership.

### 3.9 `artifacts`

| Column | Contract |
| --- | --- |
| `id` | UUID primary key |
| `case_execution_id`, `attempt_id` | Foreign keys; attempt may be null for case-level artifacts |
| `artifact_type` | Final failure screenshot, flaky failure screenshot, flaky pass screenshot, trace, download, or log |
| `relative_path` | Path beneath `results/artifacts/` |
| `checksum`, `size_bytes` | Integrity metadata |
| `created_at` | UTC timestamp |
| `retention_status` | Retained, missing, archived, or approved-deleted |

No credential or secret may appear in an artifact path.

### 3.10 `module_relationships`

| Column | Contract |
| --- | --- |
| `case_execution_id` | Foreign key |
| `module_id` | Hairline module ID |
| `relationship_type` | Primary or participating |

Unique contract: `(case_execution_id, module_id)`.

### 3.11 `review_events`

| Column | Contract |
| --- | --- |
| `id` | UUID primary key |
| `case_execution_id` | Foreign key |
| `previous_status`, `new_status` | Review lifecycle transition |
| `classification` | Human decision, when applicable |
| `reviewer` | Human identity/role |
| `notes` | Human-authored notes |
| `created_at` | UTC timestamp |
| `retest_required` | Boolean |

The current `case_executions.review_status` is a query convenience updated transactionally with the append-only event.

### 3.12 `related_items`

| Column | Contract |
| --- | --- |
| `id` | UUID primary key |
| `case_execution_id` | Foreign key |
| `item_type` | Bug ID, Plane task, fix reference, source change, or re-test run |
| `item_key` | External or internal identifier |
| `relationship` | Originated, duplicates, fixed-by, retested-by, or other approved relationship |

## 4. Required Indexes

At minimum, migrations must index:

- pending review status plus age;
- primary module plus review status;
- case ID plus execution time;
- run ID;
- preliminary outcome;
- generated backend record ID;
- correlation key;
- related item key.

## 5. Write and Recovery Contract

- Only one canonical writer commits SQLite transactions.
- Each case execution is committed atomically with its attempts, labels, source snapshots, datasets, generated records, and artifact metadata.
- Worker output is first written as a validated JSON recovery envelope.
- After a successful SQLite commit, the envelope may be marked committed and later removed under an approved housekeeping rule.
- A writer failure leaves the envelope available for deterministic replay.
- Replay must be idempotent using execution ID and payload checksum.

## 6. Security Contract

Before persistence, the writer must recursively redact:

- authorization and cookie headers;
- tokens and passwords;
- credential fields;
- secret configuration values;
- sensitive request/response payload fields;
- real patient information, which is prohibited at source.

Raw unredacted payloads must not be used as a recovery mechanism.

## 7. Implementation Decisions and Remaining Work

- SQLite implementation: Node built-in `node:sqlite` with a single synchronous canonical writer.
- Initial migration approach: versioned internal migrator; external migration tooling is not required for the pilot.
- Runs, executions, attempts, datasets, artifacts, review events, and the review queue are implemented for the MVP.
- Add labels, source snapshots, generated-record detail, module relationships, and external related-item links when a registered case first requires them.
- Backup location and schedule.
- Archive/retention procedure for artifacts and recovery envelopes.

The remaining operational decisions require explicit approval before long-term result retention begins.
