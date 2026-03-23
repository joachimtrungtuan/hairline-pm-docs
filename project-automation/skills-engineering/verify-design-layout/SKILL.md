---
name: verify-design-layout
description: Review completed Figma design layouts (PNG/JPG images or JSON exports) against FR screen specifications to identify missing fields, mismatched types, and flow gaps. Use when asked to "verify design", "check layout", "review screens against FR", "audit design layout", "compare Figma to spec", or "review design against requirements". Supports single FR, specific flows/screens within an FR, or multiple interconnected FRs checked together.
---

# Verify Design Layout

## Purpose

Verify completed Figma design layouts against screen specifications at the field level. Identify missing fields, wrong types, broken flow continuity, and extra unspecified elements. Output a structured report with per-flow, per-screen, per-field verdicts.

## Required Input (Non-Negotiable)

All three inputs below are **mandatory**. If any is missing or empty, **abort the operation immediately** — do not proceed, do not guess, do not improvise. Use the AskUserQuestion tool to inform the user which input is missing and ask them to provide it.

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

Specific flow(s) or screen(s) to verify. If the user does not specify scope, use the AskUserQuestion tool to ask them to confirm:

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
2. **Abort on missing input** — if any of the 3 required inputs (requirement source, scope, layout files) is missing or invalid, ABORT immediately. Do not proceed, guess, or improvise.
3. **AskUserQuestion for ALL confirmations** — every user-facing question, scope confirmation, or clarification MUST use the AskUserQuestion tool. Never assume, never print a question as plain text and wait — always use the tool.
4. **Report-first workflow** — create the report file from the template BEFORE any analysis begins. Build the skeleton with placeholders, then fill in findings incrementally as each flow/screen is completed. This ensures no findings are lost if context is exceeded.
5. **Main agent writes the report — exclusively** — only the main context agent may write to the report file. Sub-agents return findings as text; the main agent writes them into the report. This prevents write conflicts when multiple sub-agents run in parallel.
6. **Flush findings immediately** — after each sub-agent returns (or after the main agent completes a section), write the findings into the report file immediately. Do not accumulate findings in memory across multiple flows. Process one flow → write to file → move to next flow.
7. **Never load full PRD at once** — read structure first, then load only relevant sections
8. **Sub-agents use Haiku model** — all layout analysis sub-agents MUST use `model: "haiku"` to save tokens
9. **Keep main context clean** — delegate all image/JSON reading to sub-agents; main agent only orchestrates and compiles
10. **Field-level precision** — every data field in the screen spec MUST be checked individually; missing one field = documented gap
11. **Flow-first analysis** — organize work by flow, not by individual screen
12. **No silent skips** — if a layout file cannot be read or a screen has no layout, report it explicitly
13. **Report goes to `local-docs/reports/`** — follow date-folder convention (see Workflow Step 7)
14. **Evidence-backed only** — the agent must not rely on prior knowledge or assumptions about what a screen looks like or what fields it contains. Every claim (field present, field missing, field mismatched) MUST be verified against the actual layout file AND the actual requirement document. Every verdict in the report must cite its proof: the specific layout file examined and the specific spec section/field row it was checked against. If a claim cannot be backed by evidence from the provided resources, it must not appear in the report.

## Skill File Structure

| File | Purpose | When to Load |
|------|---------|-------------|
| `references/pass-fail-rules.md` | Detailed evaluation criteria, status definitions, edge cases | Before spawning sub-agents (main agent) AND included in sub-agent prompt |
| `references/sub-agent-instructions.md` | Self-contained instructions for Haiku sub-agents analyzing layouts | When constructing sub-agent prompts |
| `templates/report-template.md` | Output report template with placeholders | At Workflow Step 6 — to create the report file before analysis begins |

## Workflow

### 1. Create to-do list

**This is the very first action — no exceptions.**

Using the platform's task/todo tracking tools, create a to-do list with all workflow steps below. This list is the single source of truth. If the context window is exceeded and tasks are forgotten, the to-do list ensures nothing is skipped.

Initial to-do items:

- [ ] Parse input and confirm scope
- [ ] Read requirement source structure
- [ ] Extract flows and screens
- [ ] Inventory layout files
- [ ] Map layout files to flows and screens
- [ ] Create report file from template
- [ ] Build report skeleton
- [ ] *(Per-flow items added dynamically in Step 7)*
- [ ] Finalize report (summary dashboard + action items)
- [ ] Present summary to user
- [ ] Update log (if significant)

Mark each item in-progress when starting and completed when done.

### 2. Parse input and confirm scope

Extract FR number(s), normalize to `FR-###`. If user specified flow/screen scope, note it. If not, use AskUserQuestion to ask user to confirm:

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
4. Validate the document contains: (a) identifiable flows, (b) screen specifications, (c) data field tables. If any is missing, abort and notify user via AskUserQuestion.

### 4. Extract flows and screens

For each flow in scope:

1. Read the workflow/flow section to understand: flow name, actor, main steps, screen sequence, transitions
2. Read each screen specification: purpose, data fields table (field name, type, required, description, validation), business rules, conditional states
3. Build a **flow map**: `Flow ID → [Screen 1 → Screen 2 → ...]` with field counts per screen

### 5. Inventory and map layout files

1. Scan `layout-temp/` recursively — list all files (PNG, JPG, JSON)
2. Note subfolder structure (files may be organized by feature area, not by FR/flow)
3. Do NOT read file contents yet — only catalog paths and filenames
4. Map each layout file to the closest flow + screen using filename patterns and subfolder names:
   - Some files map 1:1 to screens (e.g., `Screen P01.2-S1_ Settings Main Screen.png`)
   - Some files combine multiple screens in one image
   - Some files represent states/variants of a screen (e.g., `Error.png`, `Empty.png`)
   - Some files may not map to any in-scope flow (note as unmapped)
   - Order may not match the flow sequence — be flexible
5. Produce a mapping table: `Layout File → Flow ID → Screen ID → Notes`

### 6. Create report file from template

1. Load `templates/report-template.md`
2. Copy it to: `local-docs/reports/YYYY-MM-DD/design-layout-verification-{scope}.md`
   - `{scope}` examples: `fr006`, `fr003-fr005`, `fr001-p01.1-p01.3`
   - If the date folder doesn't exist, create it
   - Use today's date
3. The file at this point contains **placeholders only** — this is intentional

### 7. Build report skeleton

Fill in the report file with known metadata and structure (but NOT findings yet):

1. **Header section**: Report date, FR scope, flow scope, layout source, platform — fill from Step 2–3
2. **Summary dashboard**: Create the table rows for each flow with placeholder statuses (`{TBD}`)
3. **Layout file inventory**: Fill the mapped/unmapped tables from Step 5
4. **Detailed verification sections**: For each flow, create the flow header and screen sub-headers with empty field tables (column headers only, no data rows yet)

**Write the skeleton to the report file now.** This establishes the structure that will be filled incrementally.

**Add per-flow to-do items**: For each flow in scope, add a to-do item: `Analyze and write findings: Flow {ID} — {Name}`

### 8. Analyze flows and write findings (one at a time)

**Process each flow sequentially. After each flow completes, write its findings to the report file immediately.**

For each flow in scope:

#### 8a. Spawn sub-agent for this flow

Spawn a Haiku sub-agent with:

- The screen specification text for this flow (extracted in Step 4)
- The list of layout files mapped to this flow (from Step 5)
- Full content of `references/sub-agent-instructions.md`
- Full content of `references/pass-fail-rules.md`

**Model**: Always `model: "haiku"`

If a flow has many screens (>5), consider splitting into 2 sub-agents. But even then, wait for both to return before writing.

**Note on parallelism**: You MAY spawn sub-agents for multiple flows in parallel to save time. However, you MUST still write each flow's findings to the report file one at a time (sequentially) to avoid write conflicts. The pattern is: spawn multiple → collect results → write Flow A → write Flow B → write Flow C.

#### 8b. Receive and validate sub-agent findings

1. Receive structured results from the sub-agent
2. Validate completeness: every screen in this flow must have a verdict
3. Apply pass/fail rules from `references/pass-fail-rules.md` to compute:
   - Field-level status (✅ / ⚠️ / ❌⚠️ / ❌ / ➕)
   - Screen-level status (🟢 COMPLETE / 🟢 GOOD / 🟡 PARTIAL / 🔴 FAIL / ⬜ NO DESIGN)
   - Flow-level status (🟢 COMPLETE / 🟡 PARTIAL / 🔴 BLOCKED)

#### 8c. Write findings to report file (main agent only)

1. Open the report file
2. Replace the placeholder section for this flow with the actual findings:
   - Per-screen field tables with statuses and notes
   - Screen status and field coverage
   - Flow coverage gaps
3. Update the summary dashboard row for this flow (replace `{TBD}` with actual status)
4. **Save the file**

**Mark the flow's to-do item as completed.**

**Do NOT hold findings in memory for later — flush to file now.**

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
