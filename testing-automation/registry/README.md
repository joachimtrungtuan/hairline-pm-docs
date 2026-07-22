# Test Case Registry

**Status:** Provider login suite active; first Team directory and invitation-management suite registered as draft
**Governing document:** `local-docs/testing-automation/TESTING-CONSTITUTION.md`
**Manual execution:** `local-docs/testing-automation/OPERATIONS.md`

This folder will contain the human-reviewed web E2E registry organized by tenant, primary Hairline module, and then function or flow.

The registry must reference live source documents under `local-docs/`; it must not copy system PRDs, functional PRDs, module definitions, or product-plan requirements.

## Registration Gate

Every new function or flow starts with a low-token PRD scout:

1. Read only the relevant PRD's module scope and overall business workflows.
2. Return a concise proposed flow and open questions.
3. Stop for Product Owner corrections, operational input, and explicit approval of the function boundary and canonical happy path.
4. Under Testing Constitution v1.2, derive the remaining applicable cases from the PRDs and verified implementation behavior without requiring case-by-case approval.
5. Register happy, negative, validation, boundary, permission, state-transition, and other applicable cases together; mark non-applicable categories and governed coverage gaps explicitly.

Do not perform detailed discovery speculatively before the human flow gate.

No module folders, case files, datasets, or Playwright specs should be created until:

1. the PRD flow scout is complete;
2. the Product Owner has corrected and approved the function boundary and canonical happy path.

After that gate, unambiguous PRD-derived cases may be registered and activated after deterministic validation. Stop for human direction when requirements conflict or are ambiguous, setup would be unsafe/destructive, deterministic execution is unavailable, or the proposed case changes the approved function boundary or expected product outcome.

Cross-module flows will have one primary owning module and explicit participating-module relationships.

## Registered Modules

- `provider/PR-01-auth-team-management/` — Six Provider login cases are active. Eighteen Team directory and invitation-management cases are registered as draft, including matching/empty search and individual/combined filter coverage, with governed fixture and isolation gaps documented in their function registry.

Contracts:

- `IDENTIFIERS.md` — stable human-facing IDs and revision rules.
- `CASE-TEMPLATE.md` — initial function/flow case registry template.
