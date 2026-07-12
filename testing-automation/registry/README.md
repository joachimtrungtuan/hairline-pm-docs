# Test Case Registry

**Status:** Identifier and case-template contracts defined; no cases registered
**Governing document:** `local-docs/testing-automation/TESTING-CONSTITUTION.md`

This folder will contain the human-reviewed web E2E registry organized by tenant, primary Hairline module, and then function or flow.

The registry must reference live source documents under `local-docs/`; it must not copy system PRDs, functional PRDs, module definitions, or product-plan requirements.

## Registration Gate

Every new function or flow starts with a low-token PRD scout:

1. Read only the relevant PRD's module scope and overall business workflows.
2. Return a concise proposed flow and open questions.
3. Stop for Product Owner corrections, operational input, and explicit flow approval.
4. Only then inspect detailed screen requirements, live UI/API behavior, datasets, roles, edge cases, and test cases.

Do not perform detailed discovery speculatively before the human flow gate.

No module folders, case files, datasets, or Playwright specs should be created until:

1. the PRD flow scout is complete;
2. the Product Owner has corrected and approved the flow;
3. the detailed registration proposal receives human approval.

Cross-module flows will have one primary owning module and explicit participating-module relationships.

Contracts:

- `IDENTIFIERS.md` — stable human-facing IDs and revision rules.
- `CASE-TEMPLATE.md` — initial function/flow case registry template.
