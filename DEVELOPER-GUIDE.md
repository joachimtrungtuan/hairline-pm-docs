# Hairline Developer Guide

For developers and their AI agents. It tells you where the code and the requirements live, in what order to read them, and how to use the requirements graph to see how the system fits together.

All paths below are relative to the root of the docs repository (`hairline-pm-docs`). In the product team's workspace the same repository is mounted as `local-docs/`.

## 1. Repositories

| What | Address | Stack | Default branch |
|---|---|---|---|
| Requirements and docs (this repository) | https://github.com/joachimtrungtuan/hairline-pm-docs | Markdown, SQLite graph | `main` |
| Backend API (all three tenants) | https://github.com/samasu-digital/hairline-backend | Laravel | `main` |
| Web dashboards (Provider and Admin) | https://github.com/samasu-digital/hairline-frontend | Web frontend | `main` |
| Patient mobile app | https://github.com/samasu-digital/hairline-app-2 | Flutter | `main` |

Three tenants share one backend: Patient (mobile app), Provider (web), Admin (web). Module codes group the features: Patient `P-01..P-08`, Provider `PR-01..PR-07`, Admin `A-01..A-10`, Shared services `S-01..S-06`.

## 2. What is authoritative

| Question | Source | Notes |
|---|---|---|
| What must feature X do? | `project-requirements/functional-requirements/frNNN-*/prd.md` | The PRD wording is the requirement. |
| What holds across all features? | `project-requirements/system-prd.md`, section "Platform-Wide Rules" (`REQ-SYS-001` to `REQ-SYS-014`) | Cited by FRs, not repeated in them. |
| What principles and security rules can never be broken? | `project-requirements/constitution.md`, Parts A and B | Rule ids `C-…`. |
| How do the pieces connect (data, rules, screens, flows, other FRs)? | `project-requirements/graph/` | Built from the PRDs. If graph and PRD differ, the PRD wins; report the difference. |
| Why was something decided? | `project-requirements/sources/source-register.md`, then one source record | Each rule's sources are linked in the graph by `decided by`. |
| What changed recently? | A PRD's "Appendix: Change Log"; `project-requirements/update-logs/README.md` | Read history only when the reason matters. |

Not authoritative: `archived/technical-docs/` (the former technical spec and data schema, frozen 2026-10-28, kept as history), `reports/`, `project-requirements/transcriptions/` (raw client input, already folded into the PRDs).

There is no separate data schema document. Entities, fields, data types and enum values are defined in the graph (section 5) and shown in each PRD's screen tables.

## 3. Get the big picture (about one hour)

Read in this order. Large files are read by section: list the headings with `rg -n "^## " <file>`, then read one section.

1. `project-requirements/constitution.md`: "How to use this document" (a task table), then Part A (principles) and Part B (security and compliance). Skip Parts C to E unless you write docs.
2. `project-requirements/system-prd.md`: Executive Summary, Product Overview, User Personas, Core Workflows, then Platform-Wide Rules. The "Functional Requirements" section is a one-page summary per FR with its module codes; skim the ones in your area.
3. The lifecycle in the graph. Open the viewer (section 5.2), tab **Timelines**. It shows every stage of the product in order and who acts in each.
4. The FR list below, to see which PRD owns which part.

### FR list

| Area | FRs |
|---|---|
| Patient journey | FR-001 authentication and profile · FR-002 medical history and scan · FR-003 inquiry · FR-004 quote submission · FR-005 quote comparison and acceptance · FR-006 booking · FR-007 payment · FR-007B instalments · FR-008 travel · FR-010 treatment · FR-011 aftercare · FR-013 reviews |
| Monitoring | FR-037 monitor hair loss · FR-038 monitor transplant progress |
| Provider | FR-009 team and roles · FR-014 analytics · FR-024 treatments and packages · FR-032 dashboard settings |
| Admin operations | FR-015 provider management · FR-016 patient management · FR-017 billing and finance · FR-018 affiliates · FR-019 promotions · FR-031 admin access control |
| Admin configuration | FR-025 medical questionnaire · FR-026 app settings and security · FR-027 legal content · FR-028 regional pricing · FR-029 payment configuration · FR-030 notification rules |
| Cross-cutting | FR-012 messaging · FR-020 notifications · FR-021 localisation · FR-022 search · FR-023 data retention |
| Help and support | FR-033 help centre content · FR-034 support tickets · FR-035 patient help and support |

FR-036 has a Draft PRD written from its summary in `system-prd.md`; it waits for Product Owner approval and has open questions, so do not build it until it is approved. Folder names are `frNNN-kebab-slug`; the document is always `prd.md`.

## 4. Read one FR in detail

Every PRD has the same sections. Read them in this order:

| Step | Section | What you get |
|---|---|---|
| 1 | Header and Executive Summary | Modules, status, purpose |
| 2 | Module Scope | What each tenant can do; entry points |
| 3 | Business Workflows | Main and alternative flows, step by step |
| 4 | Business Rules | Each rule once, with its id `REQ-NNN-NNN` |
| 5 | Screen Specifications | One screen at a time. Field tables end with a `Graph field` column that gives the field id in the graph |
| 6 | Dependencies | The other FRs this one relies on |
| 7 | User Scenarios & Testing | Acceptance scenarios and edge cases; use them as test cases |

Rules of reading:

- A rule is stated in exactly one FR. Elsewhere it appears as a citation such as `(REQ-004-070)`. Follow the id to the owning FR (`REQ-004-…` is FR-004; `REQ-SYS-…` is the system PRD).
- Screen Specifications is the largest section. Read only the screen you are building.
- Before coding an FR, read the rules it cites from other FRs. The graph lists them in one command (section 5.3, "What does this FR depend on").
- The pre-2026-11 versions of the PRDs are not in this repository and must not be used.

## 5. The requirements graph

Location: `project-requirements/graph/`. `graph.db` (SQLite) holds the data; `graph.json` is the export the viewer reads; `schema.yaml` defines the types; `README.md` documents every script. Read-only use needs `/usr/bin/python3` with PyYAML, or just `sqlite3`.

Developers only read the graph. Changes go through the product team (`scripts/write.py` with a change-set file).

### 5.1 Model

Node types (id pattern in brackets):

| Type | Meaning |
|---|---|
| FR (`FR-004`) | One functional requirement; owns the nodes below |
| Stage (`STG-main-02-quote`) | A lifecycle state on a timeline |
| Actor (`ACT-provider`) | Who acts: patient, provider roles, admin roles, the system, external services |
| Entity (`ENT-quote`), Field (`ENT-quote.accepted_total`) | Data model: field name, data type, required, enum values, the rule that calculates it |
| Rule (`REQ-004-001`) | One business rule; full text in `attrs.statement` |
| Screen (`SCR-004-01`) | A screen and the fields it shows |
| Step (`STP-004-001`), Flow (`FLW-004-main`) | A flow is a start point; its path is the chain of steps |
| Event, Setting | Emitted events; configurable values that govern rules |
| Source (`SRC-…`) | The meeting, decision or document behind a rule |

Timelines: `main` (inquiry → quote → acceptance → booking → payment → treatment → aftercare → monitoring → review and close), `aftercare`, `monitoring`, `patient-account`, `provider-account`, `affiliate-account`, `provider-payout`, `provider-configuration`, `platform-admin`, and `platform` (rules that hold at every stage).

Edges you will use most:

| Edge | Reads as |
|---|---|
| Rule `applies at` Stage | When the rule is in force |
| Rule `applies to` Entity, Field, Screen, Actor or Event | What the rule constrains |
| Rule `governed by` Setting | The rule's value is configurable |
| Rule `decided by` Source | Where the rule comes from |
| Screen `shows` Field | What a screen displays, with `editable` |
| Field `calculated by` Rule | Derived values |
| Stage `reads` / `writes` Entity, Stage `emits` Event | Data and events per stage |
| Step `done by` Actor, `at` Stage, `on` Screen, `applies` Rule | One flow step in full |
| Step `next` Step | Order and branches; `condition` names the rule that picks the branch |
| FR `references` Rule | A dependency on a rule owned by another FR |

### 5.2 Viewer

```bash
cd project-requirements/graph
python3 -m http.server 8765      # then open http://localhost:8765/viewer/
```

- **Timelines** tab: the lifecycle, stage by stage, with actors.
- **By FR** tab: one FR's rules, entities with fields and enum values, events, settings, screens.
- Click any node for its attributes and all its links. Search by id or title.
- `viewer/3d.html?fr=FR-005` shows one FR as a network; `?flow=FLW-004-main` shows one flow path; `?nbr=1&hops=2#ENT-quote` shows everything within two links of a node.

### 5.3 Queries

Run from `project-requirements/graph/`. Add `--json` for machine output.

| Question | Command |
|---|---|
| Everything an FR owns | `/usr/bin/python3 scripts/query.py fr FR-004` |
| What is affected if I change this node | `/usr/bin/python3 scripts/query.py impact ENT-quote --depth 2` |
| Which rules, screens and stages touch this node | `/usr/bin/python3 scripts/query.py cites ENT-quote` |
| Stages of a timeline, in order, with actors | `/usr/bin/python3 scripts/query.py lifecycle main` |
| How a node changed and why | `/usr/bin/python3 scripts/query.py history REQ-004-001` |

Direct SQL (`sqlite3 -readonly graph.db "<query>"`), for what the script does not cover:

```sql
-- Full text of a rule
SELECT json_extract(attrs,'$.statement') FROM nodes WHERE id='REQ-004-001';

-- Data model of an entity: fields, types, required, calculating rule
SELECT name, data_type, required, calculated_by FROM fields WHERE entity_id='ENT-quote';

-- Allowed values of a field
SELECT * FROM enum_values WHERE field_id='ENT-quote.status';

-- What does this FR depend on: rules it cites from other FRs
SELECT n.owner_fr, n.id, n.title FROM edges e JOIN nodes n ON n.id=e.to_id
WHERE e.verb='references' AND e.from_id='FR-004' ORDER BY 1,2;

-- Steps of a flow, in order
WITH RECURSIVE p(id,n) AS (
  SELECT to_id,1 FROM edges WHERE from_id='FLW-004-main' AND verb='starts at'
  UNION
  SELECT e.to_id,n+1 FROM edges e JOIN p ON e.from_id=p.id WHERE e.verb='next' AND n<80)
SELECT MIN(n) AS step, p.id, title FROM p JOIN nodes USING(id) GROUP BY p.id ORDER BY 1;

-- Flows of an FR
SELECT id, title, json_extract(attrs,'$.kind') FROM nodes WHERE type='Flow' AND id LIKE 'FLW-004%';
```

Tables: `nodes(id, type, owner_fr, title, status, version, attrs)`, `fields`, `enum_values`, `edges(from_id, verb, to_id, attrs)`, `sources`, `changes`. Filter `status='active'`; retired nodes stay in the table.

## 6. Implementing a feature from the docs

1. Find the FR in the list (section 3) and read its PRD in the order of section 4.
2. `query.py fr FR-NNN` gives the inventory: rules, entities, fields, screens, steps, events, settings. Use it as the checklist of what the code must cover.
3. Take the data model from the graph (`fields`, `enum_values`). Use the field and enum names as given.
4. Take the cross-FR rules from the "depends on" query and read each one in its owning PRD.
5. Before changing shared data or a shared rule, run `query.py impact <node-id>` to see which other FRs it touches.
6. Build each flow from the Business Workflows section; the flow query gives the same steps with actor, stage, screen and rules attached.
7. Cite `REQ-…` ids in pull requests and tests so a reviewer can trace code to a rule.
8. If the PRD is silent, contradicts itself, or disagrees with the graph, do not guess. Raise it with the product team; the fix lands in the PRD and graph first.

Known gaps: the graph linter reports 24 open findings (`/usr/bin/python3 scripts/lint.py`), none of which changes a rule's wording. `project-requirements/constitution-open-items.md` lists constitution points left open; they are technical choices for the development team, not owner decisions.

## 7. For AI agents

- Start at `INDEX.md` (task → area → file → section). It also lists the project skills, which run only when a user asks.
- Never read a large PRD, `system-prd.md` or `constitution.md` whole. List headings, then read one section. Cap searches (`rg -n -m 20 <pattern> <path>`); narrow a noisy search, never widen it.
- Prefer the graph for lookups (one rule, one entity, one FR inventory, impact) and the PRD for exact wording and screen detail.
- Never load `graph.json` (about 14 MB) or dump whole tables; query `graph.db` with a filter.
- Treat the graph, the PRDs and `archived/` as read-only. Do not read `update-logs/` or git history unless asked for the reason behind a change.
- Quote rule ids (`REQ-…`, `C-…`) and file paths in every answer so a person can check it.

## 8. Other places

| Path | Content |
|---|---|
| `INDEX.md` | Full map of this repository and section scaffolds for each document type |
| `project-notes/code-map-{backend,frontend,app}.md` | Where each module lives in the three code repositories |
| `testing/` | Test strategy, manual test guides, automated suites (start at `testing/README.md`) |
| `product-plans/v<N>/` | Versioned delivery plans and phase readiness reports |
| `deferred-backlog/` | Issues the team chose to defer, with reason and revisit trigger |
| `project-requirements/implementation-backlog.md` | What is still open per FR after the 2026-11-25 clean-up: developer matters (yours to decide) and points waiting for a Product Owner decision (ask before building them). Read the lines of your FR before you build it |
| `project-requirements/templates/` | PRD and change-request templates |

## 9. Patient mobile API: endpoints to keep stable

For developers reworking the backend. The patient mobile app is being built in parallel against an agreed API collection of 96 requests. Those requests are a contract with the mobile team. The full list, and the corrections the requirements ask for, are in `reports/2026-11-25/patient-mobile-api-contract-vs-requirements-2026-11-25.md`.

While you rework the backend:

- **Do not rename, move or remove** any of the listed paths.
- **Do not rename, remove or change the type of** a request field, a response field or a status value on them. Example responses in the collection, once added, are part of the contract.
- **Add, do not change.** New fields, new optional parameters, new error codes and new requests are fine. A new request field must be optional, or the current app breaks.
- **When a change cannot be made by adding**, publish a new version of the request (as with `/v2/accept-quote`) and keep the old one working until the mobile team confirms the app has moved.
- **Before any breaking change**, raise it with the product team and the mobile team. Do not ship it and report it afterwards.
- **Internal changes are free**: tables, services, queues and admin or provider endpoints may change, as long as the listed requests still answer the same way.

Check before you merge: if your change touches a controller, route, resource or serializer behind one of the listed requests, compare the request and response with the collection.

Seven requests have an open contract decision (section 3 of the report). Leave them unchanged until that decision is recorded there.

## 10. Build order

Build in four phases, in this order. A phase starts only when the one before it works end to end. The patient app, the dashboards and the backend follow the same phases: a patient feature is built in the phase of the dashboard feature it depends on.

| Phase | Goal | FRs |
|---|---|---|
| 1. Commercial pilot | Onboard providers; take a patient from sign-up to a quote | FR-001, FR-002, FR-003, FR-004, FR-005, FR-009, FR-015, FR-024, FR-025, FR-026, FR-027, FR-031, the profile and pricing parts of FR-032, and the search (FR-022) and notifications (FR-020) these flows need |
| 2. Clinical and patient operations | Carry out a paid treatment and its aftercare safely | FR-006, FR-007, FR-007B, FR-008, FR-010, FR-011, FR-012, FR-016, FR-029, FR-034, FR-035, FR-037, FR-038, the invoice and refund parts of FR-017, and the rest of FR-020 |
| 3. Settlement and partner growth | Pay providers; open promotions and affiliates | The reconciliation and payout parts of FR-017, the provider earnings part of FR-014, FR-018, FR-019 |
| 4. Scale and optimisation | Analytics, localisation, remaining settings | The rest of FR-014, FR-013, FR-021, FR-023, FR-028, FR-030, FR-033, FR-036, and the rest of FR-022 and FR-032 |

- Phases 1 and 2 together are the core business journey. Finish both before anything in Phases 3 and 4.
- Do not start a feature from a later phase early, even if it looks small. If a current-phase feature needs a rule owned by a later-phase FR, build only that rule.
- If you are unsure which phase a piece of work belongs to, ask the product team.
