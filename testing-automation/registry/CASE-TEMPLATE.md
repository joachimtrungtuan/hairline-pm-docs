# Registered Function or Flow: `[FUNCTION_OR_FLOW_ID] [Title]`

**Template status:** Approved initial template
**Primary module:** `[MODULE_ID]`
**Participating modules:** `[MODULE_ID list or None]`
**Registry status:** `DRAFT / ACTIVE`
**Last UI-confirmed date:** `Not confirmed`

> Keep this file test-specific. Reference live PRD requirements; do not copy them into this registry.

## 1. Registry Control

| Field | Value |
| --- | --- |
| Function or flow ID | `[ID]` |
| Test level | `function / module-flow / cross-module-flow` |
| Primary module | `[MODULE_ID]` |
| Participating modules | `[IDs or None]` |
| Human owner | `[Name or role]` |
| Registry status | `DRAFT` |
| Happy-path approval | `[Approved date / Pending]` |
| Derived-case authority | `Testing Constitution v1.2 after happy-path approval / Pending` |
| Created | `[YYYY-MM-DD]` |
| Last approved revision | `Not approved` |
| Supersedes | `None` |
| Superseded by | `None` |

## 2. Live Source References

| Reference ID | Source path | Requirement / heading | Approved hash | Notes |
| --- | --- | --- | --- | --- |
| `[CASE-ID]-SRC-01` | `local-docs/project-requirements/...` | `[FR / heading]` | `Pending` | `[Why this source applies]` |

APIs inspected for setup or implementation evidence belong in Section 4 or the individual case. They are not requirement authority.

## 3. Requirement and Category Coverage

### Requirement Coverage Matrix

| Requirement or rule reference | Category | Case / gap | Coverage |
| --- | --- | --- | --- |
| `[Source reference and concise test interpretation]` | `[happy / negative / validation / boundary / permission / state transition / other]` | `[CASE-ID / GAP-ID]` | `[Complete / Partial / Open]` |

### Category Applicability

| Category | Status | Notes |
| --- | --- | --- |
| Happy path | `[Covered / Gap]` | `[Case or reason]` |
| Negative / validation | `[Covered / Not applicable / Gap]` | `[Case or reason]` |
| Boundary / edge | `[Covered / Not applicable / Gap]` | `[Case or reason]` |
| Permission / role | `[Covered / Not applicable / Gap]` | `[Case or reason]` |
| State transition | `[Covered / Not applicable / Gap]` | `[Case or reason]` |
| Idempotency | `[Covered / Not applicable / Gap]` | `[Case or reason]` |
| Concurrency-sensitive | `[Covered / Not applicable / Gap]` | `[Case or reason]` |
| Data consistency | `[Covered / Not applicable / Gap]` | `[Case or reason]` |

Record every applicable normative PRD rule as an executable case or a governed gap. A gap must state the missing fixture, isolation control, deterministic assertion, or human decision needed; never count it as passing coverage.

## 4. Current Implementation Mapping

| Surface | Current route / API | Mapping status | Last confirmed | Notes |
| --- | --- | --- | --- | --- |
| UI | `[route]` | `Unconfirmed` | `—` | `[Current implemented interaction]` |
| Setup API | `[method and endpoint]` | `Unconfirmed` | `—` | `[Synthetic prerequisite purpose]` |

## 5. Dataset Recipes

| Dataset ID | Revision | Scenario purpose | Builder reference | Retention marker |
| --- | --- | --- | --- | --- |
| `[MODULE]-DS-0001` | `v1` | `[Happy / edge / negative purpose]` | `datasets.ts#[export]` | `[run marker field]` |

Record data-generation rules and boundary values in the dataset implementation. Do not paste credentials or real patient data here.

## 6. Test Cases

### `[MODULE]-TC-0001` — `[Observable behavior]`

| Field | Value |
| --- | --- |
| Revision | `v1` |
| Status | `DRAFT` |
| Scenario category | `happy / negative / boundary / permission / state transition / other` |
| Regression tiers | `smoke / affected / module / full` |
| Priority | `[P0-P3 or approved scale]` |
| Dataset | `[DATASET-ID] v[revision]` |
| Automation | `tests.spec.ts > [CASE-ID] [test title]` |
| Last UI-confirmed date | `Not confirmed` |

#### Preconditions

- `[State required before the UI action under examination]`

#### API-assisted setup

1. `[Deterministic setup step and expected setup outcome]`

#### UI actions

1. `[Observable Playwright action]`

#### Assertions

1. `[Observable expected result linked to a source reference]`

#### Runtime evidence requirements

- `[Additional safe diagnostic required beyond the constitutional default, or None]`

#### Known approved notes

- `None`

## 7. Revision Log

| Revision | Date | Status | Reason | Approved by | Originating result / change |
| --- | --- | --- | --- | --- | --- |
| `v1` | `[YYYY-MM-DD]` | `Draft` | `Initial registration` | `Pending` | `[Run/review/source change or None]` |

## 8. Registration Checklist

- [ ] A narrow PRD flow scout was completed before detailed discovery.
- [ ] Product Owner corrections/input and explicit happy-path/function-boundary approval were recorded.
- [ ] Every applicable PRD rule is mapped to an executable case or governed coverage gap.
- [ ] Happy, negative, validation, boundary, permission, state-transition, idempotency, concurrency, and data-consistency categories are covered or marked not applicable/gap with reasons.
- [ ] Primary and participating modules are correct.
- [ ] IDs follow `registry/IDENTIFIERS.md`.
- [ ] Sources point to live PRD/product-plan sections without copied requirements.
- [ ] Current UI mapping was inspected and dated.
- [ ] APIs are treated as setup/implementation evidence, not requirement authority.
- [ ] Every case has a deterministic dataset recipe.
- [ ] UI actions do not claim to test steps bypassed by API setup.
- [ ] Assertions are observable and source-linked.
- [ ] Credentials, secrets, and real patient data are absent.
- [ ] The approved happy case and every unambiguous PRD-derived case passed deterministic validation before status became `ACTIVE`.
- [ ] Human direction was obtained for any ambiguous/conflicting expectation, unsafe setup, non-deterministic case, or changed function boundary.
