# Item Derivation

How to turn in-scope FR PRDs and the plan's phase exit gate into a frozen, ordered list of
review units. The goal is determinism: the same PRD revision and plan always yield the same
units with the same IDs, so reports are comparable across runs and resume works.

## 1. What becomes a unit

| Unit type | Source | One unit per |
|---|---|---|
| Use case | PRD headings or labels named "Use Case" (some PRDs have them) | use case |
| User story / scenario | `## User Scenarios & Testing` → `### User Story N ...` (or "Scenario N") | story or scenario |
| Main flow | `## Business Workflows` → each `### Workflow N` or `### Main Flow: ...` | workflow / main flow |
| Alternative flow | each item under an `### Alternative Flows` block (labelled `A1`, `B2` or plain bullets) | alternative flow |
| Edge case | `## Edge Cases` and `### Edge Cases (User Scenarios)`, deduplicated | distinct edge case |
| Screen | `## Screen Specifications` → Provider and Admin platform screens only, and only if not covered by a flow unit (see §4) | uncovered dashboard screen |
| Exit gate | the phase's "Exit gate" cell in the plan roadmap table | invariant |

Not units: business rules, validation rules, security/privacy rules, success criteria, data
requirements, key entities, assumptions, implementation notes. These are **check points** folded
into their parent unit (see §5). Making every rule a unit would multiply the count tenfold and
check the same code path repeatedly; folding keeps each unit a coherent end-to-end behavior.

## 2. Deterministic order

Within each FR, derive in this fixed order, and within each block keep PRD order:

1. Use cases
2. Main flows (workflows), each immediately followed by its alternative flows
3. User stories / scenarios
4. Edge cases
5. Uncovered dashboard screens (Provider platform first, then Admin)

FRs are ordered as the plan lists them under each module; modules as the plan's phase row lists
them (Provider functions first, then Admin). Exit-gate units come last, in the order the gate
cell lists them.

## 3. Stable ID scheme

`<FR>/<code>` for FR units, `<phase>-GATE/<slug>` for gates. Prefer labels printed in the PRD;
fall back to position only when the PRD has none.

| Unit type | ID | Example |
|---|---|---|
| Use case | `UC<n>` (PRD number) | `FR-003/UC2` |
| Main flow | `W<n>` (workflow number; for unnumbered "Main Flow: X" use order of appearance) | `FR-004/W3` |
| Alternative flow | PRD label when present (`A2`, `B1`); otherwise `W<n>-A<k>` (k = bullet position under that workflow's Alternative Flows; a block not attached to a workflow uses `A<k>`) | `FR-004/A2`, `FR-009/W2-A1` |
| User story | `US<n>` keeping suffixes (`US1A`) | `FR-004/US1A` |
| Edge case | `E<k>` (position in the deduplicated union: `## Edge Cases` first, then unmatched items from `### Edge Cases (User Scenarios)`) | `FR-004/E6` |
| Screen | `SCR-<slug>` from the screen title, kebab-case, platform suffix only on collision (`-provider`, `-admin`) | `FR-004/SCR-quote-detail-admin` |
| Exit gate | `P<phase>-GATE/<slug>` | `P1-GATE/provider-isolation` |

Two edge-case bullets are duplicates when they describe the same trigger and the same expected
system response; keep the first and merge any extra detail into it as a check point.

If a later PRD revision inserts a new alternative flow in the middle of an unlabelled list,
positional IDs shift. That is acceptable; the report header records the run date and the PRD is
versioned by its change log. Do not invent labels the PRD does not have.

## 4. Screen-coverage dedupe

Dashboard screens exist to serve flows, so most are exercised by a flow unit. A screen becomes
its own unit only if no flow, story, or use case unit covers it.

- A screen is **covered** when a flow/story/use-case unit's PRD excerpt names it (by screen
  number or title) as where a step happens. Fold that screen's field, action, and state
  specifications into the covering unit's check points (the first covering unit in derivation
  order), and add the screen section's line range to that unit's PRD excerpt.
- A screen is **uncovered** otherwise; create `SCR-<slug>` with the screen's whole spec as the
  excerpt.
- Patient platform screens are never units (mobile app source is out of scope). Their behavior
  is reviewed through the backend endpoints the flows call.

## 5. Folding granular rules into parent units

For each rule in `## Business Rules`, `## Functional Requirements Summary`, Security/Privacy
subsections, or a screen's validation notes:

1. Attach it as a check point to the unit whose behavior it constrains (for example a quote
   expiry rule goes to the expiry workflow, a "provider cannot see patient identity before
   payment" rule goes to the provider inquiry view flow).
2. If it constrains several units, attach it to each (it is checked in each context).
3. If it fits no unit, attach it to the FR's first main-flow unit and mark it "(unattached rule)"
   so it is still checked.

Each check point carries its PRD section reference (`§Business Rules`, `§Screen 3`) so the
checker can cite it.

## 6. Module and tenant placement

- An FR can appear in several modules (FR-004 in PR-02 and A-01). Place each unit under the
  module whose tenant performs the unit's actor: provider-actor units under the provider module,
  admin-actor units under the admin module.
- Patient-actor and system units (scheduler, notification, expiry) go under the first in-scope
  module, in plan order, that lists the FR.
- If the run scope is one module, keep only units whose actor belongs to that module's tenant,
  plus the patient/system units that the module's flows depend on. If the scope is one FR,
  keep all its units across tenants (except patient screens).
- Each unit ID appears once per run, even if two modules share the FR.

## 7. Mobile scope

`main/hairline-app/` is never read. For patient-facing flows, the unit's check points are
written as backend obligations only: the endpoint exists, enforces auth and ownership, validates
input per PRD, returns the PRD-required data and states, and triggers the right side effects.
Patient endpoints are located through `main/hairline-backend/routes/api.php`, the
`system-technical-spec.md` API sections, and the Postman collection map.

## 8. Exit-gate units

1. Read the phase's "Exit gate" cell in the plan roadmap table.
2. Split it into atomic invariants, one per clause (for Phase 1 in v2 that yields: one
   authoritative API per flow, no production fixtures, live RBAC, session revocation, provider
   isolation, pre-payment identity privacy, quote-state consistency, scheduling rules).
3. Each invariant is one unit, checked across all in-scope modules' code.
4. For module or FR scope, keep only invariants that have a code surface inside the scope; list
   the dropped ones (with "no surface in scope") in the scope question so the user sees them.
5. Gate units are reported in the body's "Phase exit gates" section, not under a module.

## 9. Unit block handed to the checker

```text
Unit: FR-004/W3 — Quote Expiry & Status Transitions
Type: Main flow
Placement: Phase 1 › PR-02 › FR-004
Tenant(s): Provider (dashboard + backend); system jobs
PRD: local-docs/project-requirements/functional-requirements/fr004-quote-submission/prd.md
Excerpt lines: 130-147 (§Business Workflows, Workflow 3); 629-674 (§Business Rules, selected)
Check points:
  1. <flow step or folded rule> (§ref)
  2. ...
Code-map pointers: <folder groups + entry-point files from the maps>
```
