# Stable Identifier Contract

**Status:** Initial approved implementation contract
**Governed by:** `local-docs/testing-automation/TESTING-CONSTITUTION.md`

## 1. Principles

- Identifiers are immutable after first approval.
- Human-facing identifiers are readable and module-first.
- Revisions are separate from identity.
- Renaming a title, UI label, or script does not change an identifier.
- A materially different behavior receives a new identifier and an explicit superseding relationship.
- Cross-module flows use the primary owning module in their identifier.

## 2. Formats

| Entity | Format | Example |
| --- | --- | --- |
| Module | Existing Hairline module ID | `PR-02` |
| Function | `<MODULE>-FN-<NNN>` | `PR-02-FN-001` |
| Module flow | `<MODULE>-MF-<NNN>` | `PR-02-MF-001` |
| Cross-module flow | `<OWNER-MODULE>-XF-<NNN>` | `PR-02-XF-001` |
| Test case | `<MODULE>-TC-<NNNN>` | `PR-02-TC-0001` |
| Dataset recipe | `<MODULE>-DS-<NNNN>` | `PR-02-DS-0001` |
| Source reference | `<CASE-ID>-SRC-<NN>` | `PR-02-TC-0001-SRC-01` |
| Case revision | `v<positive integer>` | `v1` |
| Dataset revision | `v<positive integer>` | `v2` |
| Run | `RUN-<UTC timestamp>-<8 hex>` | `RUN-20260711T143052Z-a1b2c3d4` |
| Case execution | UUID stored by SQLite | `019f...` |
| Attempt | Positive integer scoped to execution | `1`, `2`, `3`, `4` |
| Artifact | UUID stored by SQLite | `019f...` |
| Human review | UUID stored by SQLite | `019f...` |

`<MODULE>` preserves the full established module token, including its hyphen. Sequence allocation is per module and entity type.

## 3. Allocation

Before allocating a new human-facing ID:

1. locate the primary module;
2. search only that module's registry index for the entity type;
3. take the highest existing sequence and increment it by one;
4. never reuse an identifier from a retired or superseded entity;
5. record the new entity in the module index.

Concurrent registration must use a controlled allocator or human reconciliation before merge. A duplicate identifier blocks registration approval.

## 4. Revision Rules

A case revision increments when approved test-specific content changes, including:

- source references or approved source hashes;
- preconditions;
- dataset recipe selection;
- UI actions or locators;
- assertions;
- priority or regression tier;
- automation mapping.

Review notes, execution results, and related bug IDs do not revise the case definition.

A dataset revision increments when generation logic, boundary values, defaults, or required API setup changes.

## 5. File and Test Naming

- Tenant folders use lowercase stable names such as `provider/` and `admin/`.
- Module folders begin with the module ID: `PR-02-<module-name>/`.
- Function and flow folders begin with their stable ID.
- Playwright test titles begin with the test-case ID.

Example:

```text
registry/provider/PR-02-inquiry-management/
├── module.md
├── functions/PR-02-FN-001-view-inquiry-details/
│   ├── test-cases.md
│   ├── datasets.ts
│   └── tests.spec.ts
└── flows/PR-02-MF-001-inquiry-review/
    ├── test-cases.md
    ├── datasets.ts
    └── flow.spec.ts
```

## 6. Supersession

When behavior changes materially:

- keep the old ID and revision history;
- set the old entity to `SUPERSEDED` or `RETIRED` after human approval;
- create the new entity with a new ID;
- record `supersedes_id` and `superseded_by_id` relationships;
- never rewrite historical executions to point at the new entity.
