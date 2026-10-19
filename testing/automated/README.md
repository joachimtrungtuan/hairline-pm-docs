# Automated Testing

Test material for the automated tracks. Skill instructions stay in `project-automation/skills-engineering/`; the material they read and write lives here.

| Folder | What it is | Read / written by |
|---|---|---|
| [`web-e2e/`](web-e2e/) | Playwright E2E package for the Provider and Admin dashboards: constitution, architecture, registry, framework, and results | `web-e2e-register` (registry), `web-e2e-review` (results); run via `OPERATIONS.md` |
| [`api/endpoints/`](api/endpoints/) | Single-endpoint material: `collection-map.md`, `endpoint-index.md`, `endpoint-profiles/`, `datasets.json`, and upload `assets/` | `api-testing` (reads; updates index, profiles, and datasets after confirmation); `api-flow-register` (writes endpoint profiles); `api-flow-testing` (reads) |
| [`api/flows/`](api/flows/) | Multi-step API flows: `flow-index.md`, `flow-profiles/`, legacy `flow-dictionary.md` | `api-flow-testing` (reads); `api-flow-register` (writes) |
| [`android/`](android/) | Android emulator material: `datasets.json` and `flows/` (flow definitions plus `flows/flow-index.md`) | `android-emulator-qa` (datasets); `android-flow-test` (reads flows); `android-flow-register` (writes flows) |

Dated API and Android reports go to [`../results/`](../results/). Test accounts are in [`../test-data/credentials/`](../test-data/credentials/).
