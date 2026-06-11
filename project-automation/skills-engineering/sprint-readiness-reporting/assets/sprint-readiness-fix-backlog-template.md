# Sprint [N] Readiness & Fix Backlog

> Fill-in guidance: Duplicate this template at the beginning of a sprint. Use it to anchor sprint scope to the launch plan, review the real product, and list the remaining fixes needed to reach that sprint's Definition of Done. This is not a full Plane ticket tracker. Do not add separate Plane-ID columns, assignees, estimates, or implementation ownership here. Track lifecycle in `Task Status` with the approved short values, including `Task created (HAIRL-123)`, `Resolved - pending re-test`, or `Resolved - verified YYYY-MM-DD`.

---

## Document Control & Sprint Summary

> Fill-in guidance: Complete this section first so future readers know which sprint, launch-plan scope, product environment, and review pass this document represents. Copy the sprint theme, dates, working days, goal, and Definition of Done from the launch plan without changing meaning. Keep review dates exact. If multiple environments or builds were checked, list all of them.

| Field | Value |
|---|---|
| Sprint | Sprint [N] |
| Theme | [Copy from launch plan] |
| Dates | [Copy from launch plan] |
| Working days | [Copy from launch plan] |
| Goal | [Copy from launch plan] |
| Definition of Done | [Copy the sprint-level DoD bullets or summarize without changing meaning] |
| Source launch plan | `local-docs/product-plans/2026-05-13/launch-plan.md` |
| Prepared by | [Name / role / AI agent] |
| Prepared date | YYYY-MM-DD |
| Product review date(s) | YYYY-MM-DD |
| Product environment(s) checked | [Staging / production / local / build number / app version] |
| Review scope boundary | [State what was reviewed and what was not reviewed] |

---

## How To Use This Template

> Fill-in guidance: Preserve this guidance when duplicating the template unless the sprint owner intentionally adapts the workflow. The main rule is separation of concerns: this document captures sprint scope and product gaps; Plane ticket creation happens later as a separate task, and any created Plane key should be written back only as a short `Task Status` value.

- Section 1 must mirror the launch plan. Copy or summarize only what the launch plan already says. Do not add new scope, reinterpret the sprint, or silently move work between sprints.
- Section 2 is the working fix backlog. Capture issues found from real product review in enough detail that the dev team can reproduce and fix them quickly.
- Section 3 is for findings that should not distract the current sprint. Use it to prevent out-of-scope issues from being treated as sprint commitments.
- Do not add separate Plane ticket ID, assignee, estimate, or ownership fields. Those belong to the later Plane-ticket creation workflow. Track the row lifecycle only in the existing `Task Status` cell.
- Use `Review pending` for scaffold/default placeholder rows or evidence-gap reminders that still need real product review before they count as a confirmed finding.
- Use `Recorded only` for issues already confirmed from real review evidence but not yet converted into a Plane task.
- Use `Task created (HAIRL-123)` after the implementation-task and Plane creation workflow has produced the actual issue key.
- Use `Resolved - pending re-test` only when the implementation/task side reports that the issue is fixed but the affected product path has not yet been re-tested for readiness.
- Use `Resolved - verified YYYY-MM-DD` only after the affected product path has been re-tested and the re-test evidence is recorded in `Review Notes`, `Evidence Link`, or `Notes`.
- Screenshot evidence must use persistent uploaded URLs that can be revisited later. Do not use local file paths, clipboard-only image references, or temporary file links in `Evidence Link`. If a screenshot is needed but no uploaded URL is available, ask the reviewer to upload it and use `TBD` until the raw URL is provided.

### Priority Scale

> Fill-in guidance: Use this scale consistently across sprint-level blockers and module issues. If the priority is uncertain, choose the higher priority and explain the uncertainty in Notes.

| Priority | Meaning |
|---|---|
| P0 | Blocks sprint completion, staging validation, or a core end-to-end journey. |
| P1 | Major required feature gap or broken required flow for this sprint. |
| P2 | Required but contained issue that does not block the whole sprint. |
| P3 | Minor UX, copy, polish, or cleanup issue that should not block sprint completion. |

---

# 1. Sprint Scope From Launch Plan

> Fill-in guidance: This section is the scope anchor. The AI agent filling this document should read the sprint section in the launch plan first, then reproduce the relevant sprint scope here without creating discrepancies. If the launch plan is ambiguous, note the ambiguity in the relevant scope row or review note rather than resolving it silently.

## 1.1 Modules In Scope

> Fill-in guidance: List only modules that the launch plan assigns to this sprint. Keep module IDs, module names, surfaces, and FR references aligned with the launch plan. Do not add product-review findings in this table.

| Surface | Module | FR / Scope Notes | Launch Plan Reference |
|---|---|---|---|
| [Patient Mobile / Provider Web / Admin Web / Shared Service / Affiliate] | [Module ID and name] | [FR and exact scope note from launch plan] | [Heading or line reference] |

## 1.2 User Stories In Scope

> Fill-in guidance: Copy or briefly summarize the launch-plan user stories for this sprint. Group them by the same role or surface used in the launch plan. Do not add newly discovered issues here; issues belong in Section 2.

### Patient

- [Launch-plan user story]

### Provider

- [Launch-plan user story]

### Admin

- [Launch-plan user story]

### Shared Services / Platform Foundations

- [Launch-plan user story]

### Affiliate / Partner

- [Use only if this sprint has affiliate or partner scope]

## 1.3 Explicitly Deferred / Out Of Scope

> Fill-in guidance: List items that the launch plan explicitly defers, excludes, or assigns to another sprint. This prevents later reviewers from turning known deferrals into accidental current-sprint fixes.

| Item | Launch Plan Reason / Destination | Notes |
|---|---|---|
| [Deferred module, feature, flow, or sub-scope] | [Deferred to Sprint X / post-launch / out of launch scope] | [Optional clarification] |

---

# 2. Sprint Fix Backlog

> Fill-in guidance: This section should be fast to scan and easy to act on. Every issue must describe the product behavior observed during review, not a guessed technical cause. Keep each row focused on one fixable problem. If a problem needs multiple fixes across different modules, split it into separate rows or put it in Sprint-Level Blockers.

## 2.1 Sprint-Level Blockers

> Fill-in guidance: Use this section only for issues that block the sprint Definition of Done, affect multiple modules, prevent reliable testing, or break a required cross-module journey. Do not duplicate module-specific issues here unless they are true sprint blockers.
> Fill-in guidance: Add `Task Status` so future reviewers can see whether the row is still a placeholder for later review, is a confirmed issue that is only documented here, has already been converted into a Plane task, or has been resolved and verified. Use short values such as `Review pending`, `Recorded only`, `Task created (HAIRL-123)`, `Resolved - pending re-test`, or `Resolved - verified YYYY-MM-DD`. When the create-implementation-task and Plane task-creation workflow finishes, write the resulting Plane key back into this same cell instead of adding a new tracking column.
> Fill-in guidance: For long table cells, especially `Steps to Reproduce`, `Actual Outcome`, `Expected Outcome`, and `Notes`, use `<br>` line breaks inside the cell. Keep reproduction steps as numbered lines such as `1. Open...<br>2. Click...<br>3. Verify...` so the table remains readable in Markdown preview.
> Fill-in guidance: `Evidence Link` must be a persistent uploaded URL, API/log reference, or stable report path. Do not paste local screenshot paths or clipboard-only file links. If the issue needs a screenshot and the reviewer has not uploaded one yet, ask for the uploaded URL and leave `TBD` temporarily.

| Priority | Area | Issue | Steps to Reproduce | Actual Outcome | Expected Outcome | Evidence Link | Task Status | Notes |
|---|---|---|---|---|---|---|---|---|
| P0/P1/P2/P3 | [Cross-module area or journey] | [Short problem statement] | [Numbered steps or concise reproduction path] | [What the product currently does] | [What must happen for sprint DoD] | [Screenshot / video / log / report link] | [Review pending / Recorded only / Task created (HAIRL-123) / Resolved - pending re-test / Resolved - verified YYYY-MM-DD] | [Environment, build, tenant, account, uncertainty, or related context] |

## 2.2 Module Fix Backlog

> Fill-in guidance: Create one subsection per module listed in Section 1.1, even if the module has no issues. Keep the module name exactly aligned with the launch plan. Under each module, write a short review note and then list remaining fixes.

## [Module ID] - [Module Name]

> Fill-in guidance: Briefly state what was checked in the real product for this module. Mention the environment, tenant, account type, device/browser, and any important limits of the review. If no issue was found, write "No remaining fixes found in this review pass" under Remaining Fixes.

### Review Notes

- Checked areas: [Screens, APIs, flows, roles, devices, or data states reviewed]
- Current state: [Brief summary of what works and what remains risky]
- Review limits: [Anything not checked, blocked, unavailable, or requiring follow-up]

### Remaining Fixes

> Fill-in guidance: Each row should be independently understandable by a developer. Use direct product language. Avoid assigning cause unless it was verified. Evidence Link may point to a screenshot, screen recording, API response, console log, or another local report.
> Fill-in guidance: Add `Task Status` so later Plane work can distinguish rows that are still placeholders for later verification, confirmed issues that are only captured in the report, items already turned into Plane tasks, and resolved items that still need or have passed re-test. Use a short value such as `Review pending`, `Recorded only`, `Task created (HAIRL-123)`, `Resolved - pending re-test`, or `Resolved - verified YYYY-MM-DD`. When a Plane task exists, record the exact created key in this cell so the sprint report stays traceable without becoming a separate ticket tracker.
> Fill-in guidance: For long table cells, especially `Steps to Reproduce`, `Actual Outcome`, `Expected Outcome`, and `Notes`, use `<br>` line breaks inside the cell. Keep reproduction steps as numbered lines such as `1. Open...<br>2. Click...<br>3. Verify...` so the table remains readable in Markdown preview.
> Fill-in guidance: `Evidence Link` must be a persistent uploaded URL, API/log reference, or stable report path. Do not paste local screenshot paths or clipboard-only file links. If the issue needs a screenshot and the reviewer has not uploaded one yet, ask for the uploaded URL and leave `TBD` temporarily.

| Priority | Flow / Story | Issue | Steps to Reproduce | Actual Outcome | Expected Outcome | Evidence Link | Task Status | Notes |
|---|---|---|---|---|---|---|---|---|
| P0/P1/P2/P3 | [Affected flow or launch-plan user story] | [Short problem statement] | [Numbered steps or concise reproduction path] | [What happened in the product] | [What should happen based on launch plan / DoD / PRD] | [Screenshot / video / log / report link] | [Review pending / Recorded only / Task created (HAIRL-123) / Resolved - pending re-test / Resolved - verified YYYY-MM-DD] | [Environment, account, data fixture, edge case, uncertainty, or follow-up note] |

---

# 3. Not For This Sprint

> Fill-in guidance: Use this section for findings that are real but should not be fixed in the current sprint because they are deferred by the launch plan, outside launch scope, duplicate another issue, blocked by a future dependency, or too minor for the sprint goal. This keeps the sprint backlog focused.

| Item | Why It Is Not In This Sprint | Follow-Up Notes |
|---|---|---|
| [Feature, bug, polish item, or idea] | [Deferred / out of scope / duplicate / future dependency / not required for DoD] | [Where it should be revisited, if known] |
