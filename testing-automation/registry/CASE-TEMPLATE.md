# Registered Function or Flow: `[FUNCTION_OR_FLOW_ID] [Title]`

**Template status:** Approved initial template
**Primary module:** `[MODULE_ID]`
**Participating modules:** `[MODULE_ID list or None]`
**Registry status:** `DRAFT`
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
| Created | `[YYYY-MM-DD]` |
| Last approved revision | `Not approved` |
| Supersedes | `None` |
| Superseded by | `None` |

## 2. Live Source References

| Reference ID | Source path | Requirement / heading | Approved hash | Notes |
| --- | --- | --- | --- | --- |
| `[CASE-ID]-SRC-01` | `local-docs/project-requirements/...` | `[FR / heading]` | `Pending` | `[Why this source applies]` |

APIs inspected for setup or implementation evidence belong in Section 3 or the individual case. They are not requirement authority.

## 3. Current Implementation Mapping

| Surface | Current route / API | Mapping status | Last confirmed | Notes |
| --- | --- | --- | --- | --- |
| UI | `[route]` | `Unconfirmed` | `—` | `[Current implemented interaction]` |
| Setup API | `[method and endpoint]` | `Unconfirmed` | `—` | `[Synthetic prerequisite purpose]` |

## 4. Dataset Recipes

| Dataset ID | Revision | Scenario purpose | Builder reference | Retention marker |
| --- | --- | --- | --- | --- |
| `[MODULE]-DS-0001` | `v1` | `[Happy / edge / negative purpose]` | `datasets.ts#[export]` | `[run marker field]` |

Record data-generation rules and boundary values in the dataset implementation. Do not paste credentials or real patient data here.

## 5. Test Cases

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

## 6. Revision Log

| Revision | Date | Status | Reason | Approved by | Originating result / change |
| --- | --- | --- | --- | --- | --- |
| `v1` | `[YYYY-MM-DD]` | `Draft` | `Initial registration` | `Pending` | `[Run/review/source change or None]` |

## 7. Registration Checklist

- [ ] A narrow PRD flow scout was completed before detailed discovery.
- [ ] Product Owner corrections/input and explicit flow approval were recorded.
- [ ] Primary and participating modules are correct.
- [ ] IDs follow `registry/IDENTIFIERS.md`.
- [ ] Sources point to live PRD/product-plan sections without copied requirements.
- [ ] Current UI mapping was inspected and dated.
- [ ] APIs are treated as setup/implementation evidence, not requirement authority.
- [ ] Every case has a deterministic dataset recipe.
- [ ] UI actions do not claim to test steps bypassed by API setup.
- [ ] Assertions are observable and source-linked.
- [ ] Credentials, secrets, and real patient data are absent.
- [ ] Human approval is recorded before status becomes `ACTIVE`.
