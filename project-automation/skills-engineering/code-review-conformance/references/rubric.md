# Verdict and Severity Rubric

Shared by the checker, the verifier, and the main agent. Use the definitions literally; when two
labels seem to fit, pick the one with the stronger evidence requirement you can actually meet.

## Unit verdicts (one per unit, shown in the Summary)

| Verdict | Use when | Example |
|---|---|---|
| **Conforms** | Every check point is implemented in source as the PRD requires, with file:line evidence. No gaps. | Quote expiry job exists, runs on the PRD schedule, sets the PRD status, notifies the provider. |
| **Partial** | The core behavior exists, but one or more check points are missing or wrong. Has at least one gap. | Quote list paginates but ignores the PRD's status filter. |
| **Gap** | The core behavior of the unit is missing, stubbed, fixture-backed, or contradicts the PRD. | Admin quote detail screen renders a hard-coded sample quote. |
| **Needs runtime** | Static reading cannot decide, and no static gap was confirmed; a live check is required. | Ownership is enforced by a policy whose binding depends on runtime config. |
| **Needs decision** | The PRD is ambiguous or conflicts with another PRD/the plan, so conformance cannot be judged. | Two PRDs give different expiry windows. |
| **Not checked** | The unit was not reviewed. Always followed by `— <reason>` (subagent failure, malformed return twice, missing from run). | `Not checked — checker timed out` |

A unit's verdict follows its worst surviving gap: any Confirmed gap affecting the core behavior
gives **Gap**; Confirmed gaps on secondary check points give **Partial**; only Needs runtime /
Needs decision gaps give that verdict.

## Gap status (one per gap, shown in the body)

| Status | Meaning | Consumed by create-bug-tasks? |
|---|---|---|
| **Confirmed** | Code evidence (file:line) or a probe shows the PRD requirement is not met, and the verifier could not refute it. | Yes |
| **Needs runtime** | A plausible defect that only a live run can prove or disprove. | No (skipped) |
| **Needs decision** | A human must decide what the PRD means or which source wins. | No (skipped) |

A gap without a file:line pointer **and** a PRD section reference cannot be Confirmed.

## Severity (gap priority, maps directly to create-bug-tasks Priority)

| Priority | Use when | Examples |
|---|---|---|
| **P0** | Security, privacy, money, or data-integrity defect; cross-tenant access; or an exit-gate invariant fails. | Provider can fetch another provider's inquiry; patient identity exposed before payment; production fixture shown as live finance data. |
| **P1** | A PRD main flow or state transition is broken, missing, or contract-mismatched so the feature does not work as specified. | Quote status hard-coded; dashboard calls a route the backend does not define. |
| **P2** | An alternative flow, edge case, validation, or secondary requirement is missing or wrong; the main flow still works. | Draft auto-archive after 7 days not implemented; overlap validation missing on one path. |
| **P3** | Minor: copy, labels, ordering, non-blocking UI detail. | Column label differs from PRD; default sort differs. |

## Verifier outcomes

| Outcome | Meaning |
|---|---|
| **Confirmed** | Searched the alternative locations listed in the verifier brief; the gap stands as stated. |
| **Downgraded** | The gap stands but is weaker: lower severity, or Confirmed becomes Needs runtime because the evidence is indirect. State the new severity/status. |
| **Refuted** | Found the behavior implemented elsewhere (with file:line), or showed the PRD does not require it. The gap is dropped from the body and logged once in "Refuted findings". |
