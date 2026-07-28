# E2E Status Taxonomy and Timestamp Integrity

**Date:** 2026-07-16
**Scope:** `local-docs/testing-automation/`
**Approved by:** Product Owner

## Summary

Centralized every persisted or CLI-visible testing enum in `testing-automation/status-taxonomy.json`. The runtime registry, result-envelope validator, human-review CLI, and SQLite result store now load or synchronize against that single file. `POSSIBLE_UI_DISCREPANCY` is an active governed human classification for functioning UI whose visible contract may differ from an approved requirement.

SQLite schema migration version 2 added a synchronized enum catalog, taxonomy-sync history, database validation triggers, and future run/attempt/dataset timestamps. Existing historical rows remain preserved; timestamp fields that did not exist when those rows were written remain `NULL` rather than receiving fabricated values.

## Structural Changes

- Added the centralized taxonomy and runtime loader/checksum validation.
- Aligned the runtime with all seven governed test-case registry statuses.
- Rejected unknown or inactive human classifications in both the CLI/runtime and SQLite.
- Added run finish/duration, attempt start/finish/duration, and dataset-setup start/finish/duration fields.
- Advanced the result envelope to schema version 2.
- Migrated the live result database to schema version 2 without deleting or rewriting historical executions.
- Amended the Testing Constitution to version 1.3 and aligned the operations and runner contracts.

## Verification

- `pnpm test:unit`: 40 tests passed.
- Live SQLite migration record: version 2, `status-taxonomy-and-timestamps-v2`.
- Live enum audit: existing registry, outcome, review, attempt, dataset, artifact, and human-classification values are represented by the taxonomy.
- Live timestamp schema audit: the new test-run, attempt, and execution-dataset timing columns are present.
- Team search cases no longer inspect URL or API request parameters. Their contract is limited to the visible matching, restored, or empty-state result required by the PRD.
- Corrected TC0019 validation waited for the Team directory to load and produced one consistent `POTENTIAL_ISSUE / NEEDS_HUMAN_REVIEW` execution across four timestamped attempts. Only the final-attempt screenshot and trace were retained under `RUN-20260716T050857Z-7cfbba33`.

## Minor Follow-up Updates

- 2026-07-28: Added `joachimtrungtuan.work+10@gmail.com` as patient test account `P6` in `local-docs/testing-plans/testing-credentials/patient-accounts.md`.
