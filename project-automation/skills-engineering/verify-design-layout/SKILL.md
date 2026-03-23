---
name: verify-design-layout
description: Review completed Figma design layouts (PNG/JPG images or JSON exports) against FR screen specifications to identify missing fields, mismatched types, and flow gaps. Use when asked to "verify design", "check layout", "review screens against FR", "audit design layout", "compare Figma to spec", or "review design against requirements". Supports single FR, specific flows/screens within an FR, or multiple interconnected FRs checked together.
---

# Verify Design Layout

## Required Input (Non-Negotiable)

All three inputs below are **mandatory**. If any is missing or empty, **abort the operation immediately** — do not proceed, do not guess, do not improvise. Ask the user to provide the missing input using the AskUserQuestion tool (Claude Code) or equivalent.

### 1. Requirement source (at least one)

The document containing flows, screens, and data field specifications. Accepted sources:

| Source Type | Path Pattern | Example |
|-------------|-------------|---------|
| **FR PRD** | `local-docs/project-requirements/functional-requirements/fr###-*/prd.md` | FR-006 Booking & Scheduling |
| **Report with specs** | `local-docs/reports/YYYY-MM-DD/*.md` | Missing flows design complement report |
| **Other spec document** | Any `.md` file with flow + screen + field definitions | Ad-hoc spec, technical spec, etc. |

For FR documents: accept `FR-001`, `FR001`, `fr-001`, `001` — normalize to `FR-###`.

For non-FR documents: the user provides the file path. The document must contain identifiable flows and screen specifications with data fields to be usable.

### 2. Scope

Specific flow(s) or screen(s) to verify. If the user does not specify scope, ask the user to confirm (AskUserQuestion tool in Claude Code, or equivalent):

- Full document check (all flows + screens), OR
- Specific flows (e.g., "Workflow 2 only"), OR
- Specific screens (e.g., "Screen 3 and Screen 4")

### 3. Layout files

Files in `layout-temp/` at project root. Accepts PNG, JPG (image), or JSON (Figma export). The folder structure and contents change per task — always scan fresh.

**Abort condition**: If `layout-temp/` is empty or contains no files relevant to the scope, abort and notify the user.

### Paths

```md
Layout source:     <project-root>/layout-temp/
FR documents:      local-docs/project-requirements/functional-requirements/fr###-*/prd.md
Reports:           local-docs/reports/YYYY-MM-DD/*.md
Other specs:       user-provided path
```

Where `<project-root>` is the repository root (same level as `local-docs/`, `main/`, `CLAUDE.md`).

## Hard Rules

1. **To-do list before everything** — the agent MUST create a to-do list (using the platform's task/todo tools) as the very first action, before reading any file or doing any work. Every subsequent step must be tracked in this list. The agent may exceed its context window and forget tasks — the to-do list is the single source of truth for what remains. Never do anything without a to-do list.
2. **Abort on missing input** — if any of the 3 required inputs (requirement source, scope, layout files) is missing or invalid, ask the user to provide the missing input and explain why it is needed. Use the AskUserQuestion tool (Claude Code) or the platform's equivalent interactive prompt. If the user provides it, proceed. If the user declines or insists on not providing it, ABORT the operation. Do not proceed, guess, or improvise without all 3 inputs.
3. **Ask user for ALL confirmations** — every user-facing question, scope confirmation, or clarification MUST use the AskUserQuestion tool (Claude Code) or the platform's equivalent interactive prompt. Never assume the answer, never output a question as plain text and wait.
4. **Report-first workflow** — create the report file from the template BEFORE any analysis begins. Build the skeleton with placeholders, then fill in findings incrementally as each flow/screen is completed. This ensures no findings are lost if context is exceeded.
5. **Main agent writes the report — exclusively** — only the main context agent may write to the report file. Sub-agents return findings as text; the main agent writes them into the report. This prevents write conflicts when multiple sub-agents run in parallel.
6. **Flush findings immediately** — after each sub-agent returns (or after the main agent completes a section), write the findings into the report file immediately. Do not accumulate findings in memory across multiple flows/screens. Process one unit → write to file → move to next unit.
7. **Strict linear progression — no backtracking** — process each unit (flow or screen) in sequence: load spec → find layout files → analyze → write report → mark complete → move to next. Once a unit's findings are written to the report file, that unit is CLOSED. Do not revisit, re-read, or revise a completed unit. Do not go back and forth between units to "improve" or "cross-check". Each unit is self-contained and finalized when written.
8. **Choose granularity at the start** — before beginning analysis, the agent MUST decide the processing granularity based on the task scope:
   - **Multiple flows** → process **flow by flow** (each flow is one unit)
   - **Single flow with multiple screens** → process **screen by screen** (each screen is one unit)
   - This decision is made once in Step 4 and does not change during execution.
9. **Never load full PRD at once** — read structure first, then load only relevant sections. Spec content for each unit is loaded only when that unit's turn comes — not before.
10. **Sub-agents use low-cost model** — all layout analysis sub-agents MUST use `model: "haiku"` (Claude Code) or the platform's equivalent low-cost model. The sub-agent only needs to read images/JSON and produce structured field-by-field findings — it does not need the most powerful model.
11. **Keep main context clean** — delegate all image/JSON reading to sub-agents; main agent only orchestrates and compiles
12. **Field-level precision** — every data field in the screen spec MUST be checked individually; missing one field = documented gap
13. **No silent skips** — if a layout file cannot be read or a screen has no layout, report it explicitly
14. **Report goes to `local-docs/reports/`** — follow date-folder convention (see Workflow Step 7)
15. **Evidence-backed only** — the agent must not rely on prior knowledge or assumptions about what a screen looks like or what fields it contains. Every claim (field present, field missing, field mismatched) MUST be verified against the actual layout file AND the actual requirement document. Every verdict in the report must cite its proof: the specific layout file examined and the specific spec section/field row it was checked against. If a claim cannot be backed by evidence from the provided resources, it must not appear in the report.
16. **UX/UI evaluation mandatory** — after verifying field completeness, every screen MUST also be evaluated for UX/UI design quality using the concrete checklist in `references/ux-ui-evaluation-rules.md` and the platform UX/UI skills. See Workflow Step 8d.

## Skill File Structure

| File | Purpose | When to Load |
|------|---------|-------------|
| `references/pass-fail-rules.md` | Detailed evaluation criteria, status definitions, edge cases | Before spawning sub-agents AND included in sub-agent prompt |
| `references/sub-agent-instructions.md` | Self-contained instructions for sub-agents analyzing layouts | When constructing sub-agent prompts |
| `references/ux-ui-evaluation-rules.md` | Concrete UX/UI checklist (27 universal + 10 mobile + 10 web rules), severity criteria, rule IDs | Included in sub-agent prompt alongside sub-agent-instructions.md |
| `assets/report-template.md` | Output report template — copied and filled per task | At Workflow Step 6 — copy to `local-docs/reports/YYYY-MM-DD/` before analysis begins |

## Workflow

### 1. Create to-do list

**This is the very first action — no exceptions.**

Using the platform's task/todo tracking tools, create a to-do list with all workflow steps below. This list is the single source of truth. If the context window is exceeded and tasks are forgotten, the to-do list ensures nothing is skipped.

Initial to-do items:

- [ ] Parse input and confirm scope
- [ ] Read requirement source structure
- [ ] Build processing plan (flows/screens list + decide granularity)
- [ ] Inventory layout files and build mapping
- [ ] Create report file from template
- [ ] Build report skeleton
- [ ] *(Per-unit items added dynamically in Step 7 — one item per processing unit, each includes: LOAD → FIND → ANALYZE → WRITE → CLOSE)*
- [ ] Finalize report (summary dashboard + action items)
- [ ] Present summary to user
- [ ] Update log (if significant)

Mark each item in-progress when starting and completed when done.

### 2. Parse input and confirm scope

Extract FR number(s), normalize to `FR-###`. If user specified flow/screen scope, note it. If not, ask the user to confirm (AskUserQuestion tool in Claude Code, or equivalent):

- Full FR check (all flows + screens), OR
- Specific flows (e.g., "Workflow 2 only"), OR
- Specific screens (e.g., "Screen 3 and Screen 4")

For multi-FR mode, confirm which FRs and whether they share flows to check together.

### 3. Read requirement source structure

**For FR PRD:**

1. Locate `local-docs/project-requirements/functional-requirements/fr###-*/prd.md`
2. Read first 30 lines for metadata (module, status, platform)
3. Extract H2/H3 headers with line numbers to map document structure
4. Identify: **Business Workflows** section (flow definitions) and **Screen Specifications** section (field tables)

**For report or other spec document:**

1. Read the user-provided file path
2. Read first 30 lines for metadata
3. Extract section headers to identify flow definitions and screen/field tables
4. Validate the document contains: (a) identifiable flows, (b) screen specifications, (c) data field tables. If any is missing, abort and notify the user (AskUserQuestion tool in Claude Code, or equivalent).

### 4. Build processing plan (structure only — do NOT load spec content)

**Purpose**: Determine what units to process and in what order. Do NOT read full spec content yet — only extract the structure.

1. From the requirement source, extract the **list of flows and their screens** (names, IDs, line number ranges). Read only headers and structure — not the full data fields tables.
2. Build a **flow map**: `Flow ID → [Screen 1, Screen 2, ...]` — names and IDs only, no field details yet.
3. **Decide processing granularity** (this decision is final):
   - If scope includes **multiple flows** → each flow is one processing unit
   - If scope includes **one flow with multiple screens** → each screen is one processing unit
4. **Build the processing queue**: an ordered list of units to process, one by one.

### 5. Inventory layout files (catalog only — do NOT read contents)

1. Scan `layout-temp/` recursively — list all files (PNG, JPG, JSON)
2. Note subfolder structure (files may be organized by feature area, not by FR/flow)
3. Do NOT read file contents yet — only catalog paths and filenames
4. Produce a preliminary mapping using filename patterns and subfolder names:
   - Some files map 1:1 to screens (e.g., `Screen P01.2-S1_ Settings Main Screen.png`)
   - Some files combine multiple screens in one image
   - Some files represent states/variants of a screen (e.g., `Error.png`, `Empty.png`)
   - Some files may not map to any in-scope flow (note as unmapped)
   - Order may not match the flow sequence — be flexible
5. Produce a mapping table: `Layout File → Flow ID → Screen ID → Notes`

### 6. Create report file from template

1. Load `assets/report-template.md` (located at `local-docs/project-automation/skills-engineering/verify-design-layout/assets/report-template.md`)
2. Determine the report file path using this exact formula:

   **Directory**: `local-docs/reports/YYYY-MM-DD/` where `YYYY-MM-DD` is today's date. If the directory does not exist, create it.

   **Filename**: `design-layout-verification-{scope}.md` where `{scope}` is built as follows:

   | User input | `{scope}` value | Full filename example |
   |------------|----------------|----------------------|
   | Single FR (e.g., FR-006) | `fr006` | `design-layout-verification-fr006.md` |
   | Multiple FRs (e.g., FR-003, FR-005) | `fr003-fr005` (hyphen-separated, ascending order) | `design-layout-verification-fr003-fr005.md` |
   | Single FR with specific flows (e.g., FR-001 flows P01.1–P01.3) | `fr001-p01.1-p01.3` | `design-layout-verification-fr001-p01.1-p01.3.md` |
   | Non-FR document | lowercase slug from document title, max 50 chars | `design-layout-verification-missing-flows-audit.md` |

   **Full path**: `local-docs/reports/YYYY-MM-DD/design-layout-verification-{scope}.md`

3. Copy the template content to this path. The file at this point contains **placeholders only** — this is intentional.

### 7. Build report skeleton

Fill in the report file with known metadata and structure (but NOT findings yet):

1. **Header section**: Report date, FR scope, flow scope, layout source, platform — fill from Step 2–3
2. **Summary dashboard**: Create the table rows for each flow with placeholder statuses (`{TBD}`)
3. **Layout file inventory**: Fill the mapped/unmapped tables from Step 5
4. **Detailed verification sections**: For each flow, create the flow header and screen sub-headers with empty field tables (column headers only, no data rows yet)

**Write the skeleton to the report file now.** This establishes the structure that will be filled incrementally.

**Add per-flow to-do items**: For each flow in scope, add a to-do item: `Analyze and write findings: Flow {ID} — {Name}`

### 8. Process each unit (strict linear sequence — no backtracking)

Process units from the queue built in Step 4, **one at a time**, in order. Each unit follows the exact same 5-phase cycle. Once a unit is written to the report, it is **CLOSED** — never revisited.

**The cycle for each unit (flow or screen):**

```md
LOAD spec → FIND layout files → ANALYZE → WRITE to report → CLOSE (mark complete, move on)
```

**Do not start the next unit until the current one is fully written and closed.**

#### 8a. LOAD — Read the spec for this unit only

**Always load two layers of context:**

1. **Flow context (the user journey)**: The workflow/flow section that describes the end-to-end user journey — what steps the user takes, in what order, what triggers each transition, what the user's goal is. This provides the broader picture of *why* each screen exists, *how the user arrives at it*, and *where they go next*. Without this, field-level checks happen in a vacuum and miss logical gaps.

2. **Screen spec (the data fields)**: The screen specification with data fields tables, business rules, conditional states.

**How to load per unit type:**

- If the unit is a **flow**: read the flow's workflow section (user journey, steps, transitions) + all screen specifications within it (data fields tables, business rules, conditional states). Use targeted reads with line number offsets from Step 4 — do not re-read the full document.
- If the unit is a **screen**: read that screen's specification section (data fields table, business rules, conditional states) AND also read the parent flow's workflow section to understand the user journey leading up to and out of this screen. The flow context is essential even when processing screen-by-screen — the sub-agent must know what happened before this screen and what happens after.

**Do NOT load specs for other units at this stage.** Only the current unit's spec (+ its flow context) is in memory.

#### 8b. FIND — Identify layout files for this unit

From the mapping table built in Step 5, pull the layout files that correspond to this unit. Confirm the files exist. If no layout files map to this unit, the unit's status is ⬜ NO DESIGN — write that to the report and move on.

#### 8c. ANALYZE — Spawn sub-agent and receive findings

Spawn a sub-agent with:

- The **flow context** (user journey, steps, transitions) loaded in 8a — so the sub-agent understands the broader UX flow
- The **screen spec text** loaded in 8a (data fields, business rules, conditional states)
- The layout file paths identified in 8b
- Full content of `references/sub-agent-instructions.md`
- Full content of `references/pass-fail-rules.md`
- Full content of `references/ux-ui-evaluation-rules.md`

**Model**: Always use `model: "haiku"` (Claude Code) or the platform's equivalent low-cost model.

If a flow unit has many screens (>5), consider splitting into 2 sub-agents. Wait for all to return before proceeding to 8d.

On receiving results:

1. Validate completeness: every screen in this unit must have a verdict
2. Apply pass/fail rules from `references/pass-fail-rules.md` to compute:
   - Field-level status (✅ / ⚠️ / ❌⚠️ / ❌ / ➕)
   - Screen-level status (🟢 COMPLETE / 🟢 GOOD / 🟡 PARTIAL / 🔴 FAIL / ⬜ NO DESIGN)
   - Flow-level status (🟢 COMPLETE / 🟡 PARTIAL / 🔴 BLOCKED) — if unit is a flow

#### 8d. ANALYZE (UX/UI) — Evaluate design quality

After field-level analysis, evaluate each screen's layout design quality using the concrete checklist in `references/ux-ui-evaluation-rules.md`. Every finding MUST cite a rule ID from that document — no finding based on subjective impression is acceptable.

1. **Determine which rule sections apply** based on platform (identified in Step 3):
   - Always apply Section 3 (Universal checks U-01 through U-27)
   - Mobile platforms → also apply Section 4 (Mobile checks M-01 through M-10)
   - Web platforms → also apply Section 5 (Web checks W-01 through W-10)
2. **Invoke the platform's UX/UI skills** for additional expertise:
   - Always invoke `ui-ux-pro-max`
   - Additionally invoke `mobile-design` for mobile platforms
   - Additionally invoke `web-design-guidelines` for web platforms
3. **Run every applicable rule** from `references/ux-ui-evaluation-rules.md` against the layout. For each rule: evaluate → PASS (omit from report) or ISSUE → assign severity using Section 2 criteria
4. **Collect UX/UI findings** per screen: each finding must include rule ID, severity (from Section 2 criteria — not intuition), observation, and evidence (which layout file, what was seen)

#### 8e. WRITE — Write all findings to report file (main agent only)

1. Open the report file
2. Replace the placeholder section for this unit with the actual findings:
   - Per-screen field tables with statuses and notes
   - Screen status and field coverage
   - UX/UI Design Evaluation subsection per screen
   - Flow coverage gaps (if unit is a flow)
3. Update the summary dashboard row for this unit (replace `{TBD}` with actual status)
4. **Save the file**

**Do NOT hold findings in memory for later — flush to file now.**

#### 8f. CLOSE — Mark complete and move on

1. Mark this unit's to-do item as **completed**
2. **Discard** the spec content and sub-agent findings from memory — they are in the report file now
3. **Move to the next unit** in the queue
4. **Do NOT go back** to any previously completed unit for any reason — no re-reading, no revising, no cross-checking against earlier units

### 9. Finalize report

After all flows are written:

1. Fill in the **overall summary** line in the summary dashboard
2. Compile the **Action Items** table: gather all critical/important/suggestion issues across flows, sorted by priority
3. Fill in the **Notes** section
4. Save the final report file

### 10. Present summary to user

Output a concise summary to the user:

- Overall status per flow (dashboard table)
- Count of critical issues (🔴 fields)
- Top 3–5 action items
- Full report path for reference

### 11. Update log (if significant)

If this is a major verification (full FR or multiple flows), create an update log entry per the project's update log protocol at `local-docs/project-requirements/update-logs/YYYY-MM-DD/`.
