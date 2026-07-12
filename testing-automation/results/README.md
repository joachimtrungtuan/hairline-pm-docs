# Test Results and Artifacts

**Status:** SQLite schema implemented and integration-tested; runtime database intentionally absent until the first registered test
**Governing document:** `local-docs/testing-automation/TESTING-CONSTITUTION.md`

This folder is reserved for the canonical SQLite execution/review database and module/run-organized filesystem artifacts.

Planned runtime layout:

```text
results/
├── test-results.sqlite
└── artifacts/
    └── <tenant>/<module-id>/<run-id>/<case-id>/
```

The SQLite database, screenshots, traces, downloads, and runtime logs should normally remain untracked generated assets. Schema definitions and migrations belong in version-controlled framework source once approved.

Unit tests create temporary SQLite databases outside this folder. The canonical `results/test-results.sqlite` database and artifact directory will be created by the first registered test run.

Contract:

- `SQLITE-SCHEMA.md` — conceptual relational tables, constraints, indexes, serialized-write, recovery, and redaction requirements.
