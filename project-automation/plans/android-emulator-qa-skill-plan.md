# Plan: Android Emulator QA Skill

## Context

The Hairline project has 3 tenants to test: patient mobile app (Flutter Android), provider dashboard, and admin dashboard. Dashboards already have Playwright automation. The mobile app is the gap — all testing is manual and repetitive (form filling, file/image picking, navigation flows, bug reproduction). This plan creates a cross-platform skill that automates Android emulator testing across all AI agent platforms (Claude Code, Cursor, Antigravity, Codex).

**Trigger:** OpenAI Codex recently shipped a built-in "Test Android Apps" skill with "Emulator QA" that uses ADB. We want equivalent capability on all platforms, and when on Codex, we defer to their built-in tool.

**Security constraint:** The user prioritizes security above all. A thorough audit of MCP server candidates was conducted (see Security Audit section below).

---

## Security Audit Summary

| Package | Stars | CVEs | Trust | Verdict |
|---------|-------|------|-------|---------|
| `mobile-mcp` (@mobilenext) | — | CVE-2026-35394 (intent exec), CVE-2026-33989 (path traversal, CVSS 8.1) | RED FLAG | **AVOID** |
| `maestro-mcp` (slapglif) | 1 | — | RED FLAG | **AVOID** — unofficial fork; use official `mobile-dev-inc/maestro-mcp` instead |
| `mcp-android-emulator` (Anjos2) | Low | None known | MEDIUM | Dev-only — insufficient audit data |
| **`android-mcp-server`** (minhalvp) | **709** | **None** | **HIGH** | **PRIMARY — USE** |
| **`replicant-mcp`** (thecombatwombat) | — | **None** | **HIGH** | **SECONDARY — USE** (production-grade, blocks dangerous commands) |

**Decision:** Use `android-mcp-server` (Python, 709 GitHub stars, thin ADB wrapper, active maintenance, no known vulnerabilities) as the primary MCP server for non-Codex platforms.

**Fallback:** `replicant-mcp` (Node.js, accessibility-first, token-optimized, blocks dangerous commands like `rm -rf /`, `reboot`, `su`).

**Post-install mandatory:** Run `pip audit` (or `npm audit` for replicant) before first use. Pin exact versions in config.

---

## Cross-Platform Strategy

```
┌─────────────────────────────────────────────────────┐
│              SKILL.md (Source of Truth)              │
│  Tool-agnostic workflow + tool mapping table         │
├──────────┬──────────┬──────────┬────────────────────┤
│ Claude   │ Cursor   │ Anti-    │ Codex              │
│ Code     │ Rule     │ gravity  │                    │
├──────────┼──────────┼──────────┼────────────────────┤
│ MCP:     │ MCP:     │ MCP:     │ Built-in "Test     │
│ android- │ android- │ android- │ Android Apps" skill│
│ mcp-     │ mcp-     │ mcp-     │ OR raw ADB via     │
│ server   │ server   │ server   │ SKILL.md fallback  │
└──────────┴──────────┴──────────┴────────────────────┘
```

- **SKILL.md** contains a **tool mapping table** (one row per action, columns for MCP tool name and raw ADB command equivalent)
- Agent detects its platform at Step 1 and picks the right column for the rest of the workflow
- On Codex: the `openai.yaml` default_prompt instructs the agent to use the built-in "Test Android Apps" skill. SKILL.md serves as fallback if the built-in is unavailable
- No conditional branching prose — one clean workflow, one reference table

---

## Files to Create

All paths relative to `local-docs/project-automation/`.

### Core Skill (8 files)

```
skills-engineering/android-emulator-qa/
├── SKILL.md                          ← Source of truth workflow
├── agents/
│   └── openai.yaml                   ← Codex config (defers to built-in "Test Android Apps")
├── scripts/
│   ├── ui_pick.py                    ← Extract tap coordinates from UI tree XML
│   └── ui_tree_summarize.py          ← Compact readable UI tree overview
└── references/
    ├── mcp-setup.md                  ← MCP server install + config for each platform
    ├── adb-commands.md               ← Raw ADB command reference (Codex/fallback)
    └── tool-mapping.md               ← MCP tool ↔ ADB command mapping table
```

Note: No `test-flows.md` — test flows are derived ad-hoc from PRDs at runtime, not pre-defined.

### Platform Deployments (2 files)

```
commands/android-emulator-qa.md       ← Cursor rule (condensed SKILL.md)
workflows/android-emulator-qa.md      ← Antigravity workflow (ultra-condensed)
```

### Registration (user applies manually)

The implementer produces the exact lines for `CLAUDE.md` and `AGENTS.md` but does NOT edit those files. User applies manually.

**Total: 10 new files, 0 file edits by implementer**

---

## SKILL.md Outline

```
---
name: android-emulator-qa
description: >
  Automate manual testing of the Hairline Flutter Android app on an
  emulator or physical device. Supports flow validation, bug reproduction,
  form filling, and screenshot capture. Works via android-mcp-server (MCP)
  on Claude Code/Cursor/Antigravity, or via built-in "Test Android Apps"
  skill / raw ADB on Codex.
---
```

### Sections

1. **Purpose** — Bridge repetitive manual mobile testing with agent-driven automation. Three modes: flow validation, bug reproduction, form filling.

2. **Platform Detection and Tool Selection** — Run once at start:
   - If MCP tools available (e.g., `get_screenshot`, `get_uilayout`) → use MCP mode
   - If Codex built-in "Test Android Apps" available → defer to it
   - If neither → raw ADB via Bash (fallback)

3. **Required Input**
   - **Test mode**: `flow-validation` | `bug-reproduction` | `form-filling` | `screenshot-only`
   - **Test target**: Ad-hoc description from user (e.g., "test the payment flow", "check if image upload works on profile")
   - Optional: APK path, test credentials, device serial
   - The agent resolves the test target against PRD documents — no pre-defined flow list

4. **Hard Rules**
   - Create progress checklist before any emulator interaction
   - Never modify app code or backend — read-only interaction
   - Screenshot before AND after every significant interaction
   - On crash → capture logcat immediately, pause, report
   - Save screenshots to `local-docs/reports/YYYY-MM-DD/android-qa-{session-id}/`
   - Never hard-code credentials — read from testing credentials files
   - One test target per run
   - Redact sensitive data in reports with `[REDACTED]`

5. **Progress Tracking (Mandatory)** — Platform task/todo checklist before starting

6. **Tool Mapping Reference** — Table with columns: Action | MCP Tool | Raw ADB Command

   | Action | MCP Tool | Raw ADB |
   |--------|----------|---------|
   | List devices | `get_packages()` | `adb devices` |
   | Launch app | `execute_adb_command()` | `adb shell am start -n <pkg>/<activity>` |
   | Tap | `execute_adb_command()` | `adb shell input tap <x> <y>` |
   | Swipe | `execute_adb_command()` | `adb shell input swipe <x1> <y1> <x2> <y2>` |
   | Type text | `execute_adb_command()` | `adb shell input text "<text>"` |
   | Screenshot | `get_screenshot()` | `adb exec-out screencap -p > screen.png` |
   | UI tree | `get_uilayout()` | `adb exec-out uiautomator dump /dev/tty` |
   | Back key | `execute_adb_command()` | `adb shell input keyevent 4` |
   | Logcat | `execute_adb_command()` | `adb logcat -d` |
   | Install APK | `execute_adb_command()` | `adb install -r <path>.apk` |

7. **Workflow** (10 steps)
   - Step 1: Detect platform + tools, verify device connected
   - Step 2: **Research PRD** — Read user's ad-hoc test description, search `local-docs/project-requirements/` (functional-requirements, system-prd, system-technical-spec, transcriptions) for the related flow. Extract acceptance criteria, expected behavior, edge cases, and UI expectations from the PRD.
   - Step 3: **Compose testing script** — Based on PRD findings, produce a numbered testing script with: preconditions, step-by-step actions, expected results per step, and data to use (test credentials, test inputs).
   - Step 4: **CONFIRMATION GATE (MANDATORY)** — Present the testing script to the user. Do NOT proceed until the user explicitly approves. The user may modify steps, add/remove cases, or change test data. Iterate until approved.
   - Step 5: Load credentials from testing credentials files
   - Step 6: Verify app state — screenshot, navigate to starting screen if needed
   - Step 7: Execute approved test steps — per-step: action → execute → screenshot → record Pass/Fail
   - Step 8: Capture evidence package (all screenshots + final logcat)
   - Step 9: Write test report to `local-docs/reports/YYYY-MM-DD/android-qa-{slug}.md`
   - Step 10: Present summary (pass/fail ratio, defects, report path)

8. **Flutter-Specific Notes**
   - Build: `flutter build apk --release` + `adb install -r build/app/outputs/flutter-apk/app-release.apk` (NOT Gradle directly)
   - `uiautomator dump` returns sparse tree for Flutter — coordinate-based interaction is primary strategy
   - `image_picker` / `image_cropper` invoke native Android pickers (visible to ADB)
   - Payment screens (flutter_stripe) use test card numbers in staging

9. **Error Handling**
   - Device disconnect → reconnect, resume from last step
   - App crash → logcat capture, mark remaining steps N/A
   - Screenshot fails → continue with text-only record
   - Picker doesn't open → push test image via ADB to gallery, retry
   - Empty UI tree → fall back to screenshot + coordinate analysis

10. **Quality Checklist**
    - All steps have a result (Pass/Fail/Partial/N/A)
    - Every Fail/Partial has screenshot reference + notes
    - Logcat captured for any crash/anomaly
    - All screenshots indexed in report
    - No raw credentials in report
    - Defect severity assigned (Critical/Major/Minor/Cosmetic)

---

## Helper Scripts

### `scripts/ui_pick.py`
- **Purpose:** Extract center tap coordinates from UI tree XML by searching text, resource-id, or content-desc
- **Input:** XML file path + search term
- **Output:** `x,y` coordinates for direct use in `adb shell input tap`
- **Dependencies:** Python 3 stdlib only (xml.etree.ElementTree)
- **Used by:** Codex / raw ADB mode only (MCP mode doesn't need this)

### `scripts/ui_tree_summarize.py`
- **Purpose:** Create compact readable overview of UI tree, filtering to elements with non-empty text/content-desc/resource-id
- **Input:** XML file path
- **Output:** Indented summary text
- **Dependencies:** Python 3 stdlib only
- **Used by:** Codex / raw ADB mode only

---

## `agents/openai.yaml`

```yaml
interface:
  display_name: "Android Emulator QA"
  short_description: "Automate Flutter Android app testing via emulator"
  default_prompt: >
    Run emulator-based QA for the Hairline Flutter Android app.
    Use the built-in Test Android Apps skill if available,
    otherwise follow SKILL.md using raw ADB commands.
    Build: flutter build apk + adb install.
```

---

## Platform Deployment Files

### `commands/android-emulator-qa.md` (Cursor rule)

```yaml
---
description: >
  Automate Android emulator testing for the Hairline Flutter app.
  Trigger when user asks to test mobile app, reproduce a bug on
  emulator, fill forms on Android, or capture mobile screenshots.
globs:
alwaysApply: false
---
```

Content: Condensed SKILL.md — keep tool mapping table, hard rules, workflow as numbered list, Flutter notes. Target ~150-200 lines.

### `workflows/android-emulator-qa.md` (Antigravity)

```yaml
---
description: >
  Automate Android emulator testing for the Hairline Flutter app via
  android-mcp-server or raw ADB.
---
```

Content: Ultra-condensed — hard rules as bullets, tool mapping table, workflow as flat numbered list. Target ~60-80 lines.

---

## `references/mcp-setup.md` Content

### Prerequisites
- Python 3.11+
- ADB installed and in PATH (`adb version` to verify)
- Android emulator running OR physical device with USB debugging enabled
- `uv` package manager (for android-mcp-server)

### Installation (android-mcp-server)
```bash
# Clone
git clone https://github.com/minhalvp/android-mcp-server.git
cd android-mcp-server
uv sync

# Verify
adb devices  # should show your device/emulator
```

### Claude Code MCP Config
Add to `.claude/mcp.json`:
```json
{
  "mcpServers": {
    "android-emulator": {
      "command": "uv",
      "args": ["run", "--directory", "<path-to-android-mcp-server>", "main.py"],
      "env": {}
    }
  }
}
```

### Post-Install Security Check (MANDATORY)
```bash
cd android-mcp-server
pip audit           # check for known vulnerabilities
uv tree             # inspect dependency tree
```

### Fallback: replicant-mcp (Node.js)
```bash
npm install -g replicant-mcp
npm audit           # mandatory security check
```

---

## Registration in CLAUDE.md

Add to the **Skill Definitions and Locations** table:

```
| `android-emulator-qa` | Automate Flutter Android app testing on emulator via MCP or ADB | `skills-engineering/android-emulator-qa/SKILL.md` | `commands/android-emulator-qa.md` | `workflows/android-emulator-qa.md` | `agents/openai.yaml` |
```

Add to the **When to Invoke** table:

```
| "test the app", "run emulator QA", "automate mobile testing", "reproduce this bug on the app", "fill the form on Android" | `android-emulator-qa` | **BLOCKING** |
```

**Note:** CLAUDE.md is in the project root (READ-ONLY zone). User must explicitly grant an exception to edit, or apply manually.

---

## Implementation Order

| Phase | Step | File | Depends On |
|-------|------|------|------------|
| 1 — References | 1 | `references/mcp-setup.md` | — |
| 1 — References | 2 | `references/adb-commands.md` | — |
| 1 — References | 3 | `references/tool-mapping.md` | — |
| 2 — Core | 4 | `SKILL.md` | Steps 1-3 (references it) |
| 3 — Scripts | 5 | `scripts/ui_pick.py` | — |
| 3 — Scripts | 6 | `scripts/ui_tree_summarize.py` | — |
| 4 — Codex | 7 | `agents/openai.yaml` | Step 4 |
| 5 — Deploy | 8 | `commands/android-emulator-qa.md` | Step 4 |
| 5 — Deploy | 9 | `workflows/android-emulator-qa.md` | Step 4 |
| 6 — Register | 10 | Edit `CLAUDE.md` + `AGENTS.md` | Steps 4, 8, 9 |

**Phases 1 and 3 can run in parallel.** Phases 5 steps can run in parallel. Everything else is sequential.

---

## Verification

### Pre-Delivery Checks
- [ ] SKILL.md has all required sections: frontmatter, Purpose, Required Input, Hard Rules, Progress Tracking, Workflow, Error Handling, Quality Checklist
- [ ] `openai.yaml` has exactly 3 fields: `display_name`, `short_description`, `default_prompt`
- [ ] `commands/*.md` has frontmatter with `description`, `globs`, `alwaysApply`
- [ ] `workflows/*.md` has frontmatter with `description`
- [ ] Helper scripts use only Python 3 stdlib (no pip dependencies)
- [ ] CLAUDE.md skill table row matches exact column format of existing rows
- [ ] No credentials or secrets in any file

### Runtime Smoke Test (manual, by user)
1. **Install MCP server**: Follow `references/mcp-setup.md`, run `pip audit`
2. **Start emulator**: Launch Android emulator with the Hairline app installed
3. **Claude Code test**: Ask "test the Settings flow on the emulator" — verify agent creates checklist, detects MCP, takes screenshots, navigates
4. **Codex test**: Same prompt — verify agent uses built-in "Test Android Apps" or raw ADB
5. **Verify report**: Check `local-docs/reports/YYYY-MM-DD/` for correct report structure and screenshots

---

## Acceptance Criteria

Each criterion is independently verifiable. An implementation is complete only when ALL criteria pass.

### AC-1: Skill Structure Compliance
- [ ] Directory exists at `local-docs/project-automation/skills-engineering/android-emulator-qa/`
- [ ] `SKILL.md` exists with valid YAML frontmatter containing `name` and `description` fields
- [ ] `SKILL.md` contains ALL required sections: Purpose, Platform Detection and Tool Selection, Required Input, Hard Rules, Progress Tracking (Mandatory), Tool Mapping Reference, Workflow, Flutter-Specific Notes, Error Handling, Quality Checklist
- [ ] `agents/openai.yaml` exists with exactly 3 fields under `interface:`: `display_name`, `short_description`, `default_prompt`
- [ ] `scripts/ui_pick.py` exists, is executable, uses only Python 3 stdlib (no `import` of any pip package)
- [ ] `scripts/ui_tree_summarize.py` exists, is executable, uses only Python 3 stdlib
- [ ] `references/mcp-setup.md` exists with installation instructions, Claude Code MCP config JSON, and mandatory security check steps
- [ ] `references/adb-commands.md` exists with all ADB commands from the tool mapping table, each with a working example
- [ ] `references/tool-mapping.md` exists with the complete MCP tool ↔ ADB command mapping table

### AC-2: Platform Deployments
- [ ] `local-docs/project-automation/commands/android-emulator-qa.md` exists with valid frontmatter (`description`, `globs`, `alwaysApply: false`)
- [ ] Cursor rule content is a condensed version of SKILL.md (150-200 lines), retains: tool mapping table, hard rules, workflow steps, Flutter notes
- [ ] `local-docs/project-automation/workflows/android-emulator-qa.md` exists with valid frontmatter (`description`)
- [ ] Antigravity workflow is ultra-condensed (60-80 lines), retains: hard rules as bullets, tool mapping table, workflow as flat numbered list

### AC-3: Cross-Platform Strategy
- [ ] SKILL.md tool mapping table has columns for both MCP tool name AND raw ADB command for every action (list devices, launch, tap, swipe, type, screenshot, UI tree, back, logcat, install)
- [ ] Workflow Step 1 includes platform detection logic (MCP available → MCP mode; Codex built-in → defer; neither → raw ADB)
- [ ] `openai.yaml` `default_prompt` mentions both the built-in "Test Android Apps" skill and the SKILL.md fallback
- [ ] No conditional branching prose in the workflow — one linear flow that works regardless of tool choice

### AC-4: PRD-Based Ad-Hoc Testing with Confirmation Gate
- [ ] Workflow Step 2 instructs the agent to read PRD documents from `local-docs/project-requirements/` (functional-requirements, system-prd, system-technical-spec, transcriptions) to find the flow matching the user's ad-hoc description
- [ ] Workflow Step 3 instructs the agent to compose a numbered testing script with: preconditions, step-by-step actions, expected results per step, and test data
- [ ] Workflow Step 4 is explicitly labeled as **CONFIRMATION GATE (MANDATORY)** and states: "Do NOT proceed until user explicitly approves"
- [ ] No pre-defined test-flows.md file exists — all flows derived from PRDs at runtime

### AC-5: Security Requirements
- [ ] `references/mcp-setup.md` includes a "Post-Install Security Check (MANDATORY)" section with `pip audit` and `uv tree` commands
- [ ] MCP server recommendation is `android-mcp-server` by minhalvp (NOT `mobile-mcp` which has known CVEs)
- [ ] No credentials, API keys, or secrets appear in any skill file
- [ ] Hard Rules section includes: "Never hard-code credentials" and "Redact sensitive data with [REDACTED]"
- [ ] MCP config points to `~/tools/android-mcp-server/` (global, outside project repo)

### AC-6: Hard Rules and Safety
- [ ] Hard Rules section requires: progress checklist before any interaction, screenshot before AND after every significant interaction, one test target per run, crash → logcat → pause → report
- [ ] Hard Rules explicitly state: "Never modify app code or backend — read-only interaction"
- [ ] Error Handling section covers: device disconnect, app crash, screenshot failure, picker failure, empty UI tree — each with a specific recovery action

### AC-7: Flutter Specifics
- [ ] SKILL.md mentions `flutter build apk` (NOT Gradle directly) as the build command
- [ ] SKILL.md notes that `uiautomator dump` returns sparse tree for Flutter and that coordinate-based interaction is primary
- [ ] SKILL.md notes that `image_picker` / `image_cropper` invoke native Android pickers
- [ ] Scripts handle Flutter's sparse UI tree gracefully (ui_tree_summarize filters empty nodes)

### AC-8: Helper Scripts Functionality
- [ ] `ui_pick.py` accepts: XML file path + search term → outputs `x,y` coordinates
- [ ] `ui_pick.py` supports searching by: `text`, `resource-id`, AND `content-desc` attributes
- [ ] `ui_tree_summarize.py` accepts: XML file path → outputs compact indented tree of non-empty elements
- [ ] Both scripts handle malformed/empty XML input without crashing (graceful error message)
- [ ] Both scripts include a `if __name__ == "__main__"` block for CLI usage

### AC-9: Report Output
- [ ] Workflow specifies report location: `local-docs/reports/YYYY-MM-DD/android-qa-{slug}.md`
- [ ] Workflow specifies screenshot location: `local-docs/reports/YYYY-MM-DD/android-qa-{session-id}/`
- [ ] Quality Checklist requires: all steps have results, Fail/Partial have screenshots, logcat captured for crashes, no raw credentials

### AC-10: Registration Lines Provided
- [ ] Plan or a deliverable file contains the exact CLAUDE.md table row to add (skill name, purpose, all 4 platform paths)
- [ ] Plan or a deliverable file contains the exact "When to Invoke" table row with trigger patterns and BLOCKING priority
- [ ] Same for AGENTS.md if applicable

---

## Resolved Decisions

1. **CLAUDE.md / AGENTS.md registration**: User will apply these edits manually. The implementer must produce the exact lines to add (see "Registration in CLAUDE.md" section above) but NOT edit those files.

2. **Test flow strategy — PRD-based, ad-hoc with confirmation gate**:
   - No pre-defined `test-flows.md` file. Test flows are NOT extracted from the manual testing plan (which is incomplete).
   - Instead, the user describes an ad-hoc testing need each session.
   - The agent then reads the relevant PRD documents in `local-docs/project-requirements/` (the single source of truth) to find the related flow, acceptance criteria, and expected behavior.
   - The agent composes a testing script based on the PRD.
   - **Confirmation gate (MANDATORY):** Before executing any test on the emulator, the agent presents the proposed testing script to the user for review and approval. No test runs without explicit user sign-off.
   - This changes the workflow: Step 2 becomes "Research PRD + compose script" and a new Step 2.5 "Present script for user confirmation" is added.

3. **MCP server install location**: `~/tools/android-mcp-server/` (global scope, outside project repo). This keeps the Hairline repo clean and allows reuse across other projects. The MCP config in `.claude/mcp.json` points to this path.
