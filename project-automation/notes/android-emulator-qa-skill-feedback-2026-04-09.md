# Android Emulator QA — Skill Feedback Session 2026-04-09

**Session scope:** Live testing run against `local-docs/testing-plans/2026-04-09/mobile-app-manual-testing-plan.md`
**Build under test:** TBD (APK version)
**Tester:** Joachim

---

## How to Use This File

During the testing run, note any friction, confusion, incorrect behavior, or missing logic in the skill. After the session, these notes will be used to patch SKILL.md, references, and assets.

Format per entry:
- **Step:** Which SKILL.md workflow step this applies to
- **Observation:** What happened or what was unclear
- **Suggested fix:** (Optional) What should change

---

## Observations

_Add entries below as they occur during the session._

### Skill Invocation & Setup

- **Step:** Invocation
- **Observation:** The skill currently asks for APK version, new-install check, and credential source at the steps where they're needed (Steps 5–6). This forces mid-execution interruptions that break flow.
- **Suggested fix:** Add an upfront AskUserQuestion block at the very start of the skill (before Step 1) that gathers ALL session inputs in one shot: APK path (if new), whether to install/upgrade, credential file location, device serial (if needed). Nothing should require stopping mid-run to ask the user.

---

### Step 1 — Platform Detection & Device

- **Step:** Step 1
- **Observation:** 
- **Suggested fix:** 

---

### Step 2 — Testing Plan Parsing

- **Step:** Step 2
- **Observation:** 
- **Suggested fix:** 

---

### Step 2b — Flow Script Library Check

- **Step:** Step 2b
- **Observation:** 
- **Suggested fix:** 

---

### Step 3 — Compose Testing Script

- **Step:** Step 3
- **Observation:** 
- **Suggested fix:** 

---

### Step 4 — Confirmation Gate

- **Step:** Step 4
- **Observation:** 
- **Suggested fix:** 

---

### Step 5 — Load Credentials

- **Step:** Step 5
- **Observation:** Credential source determination happens here, mid-run. If the expected file doesn't exist the skill must interrupt to ask.
- **Suggested fix:** Resolve credential file path in the upfront AskUserQuestion block at invocation, not at Step 5. Step 5 becomes a pure read step with no user interaction.

---

### Step 6 — APK Installation Check

- **Step:** Step 6
- **Observation:** Step 6 asks "Is there a new version to install?" mid-execution, blocking progress. This is the clearest example of an input that should be collected upfront.
- **Suggested fix:** Fold the APK question (new install? path?) into the initial AskUserQuestion at invocation. Step 6 becomes a conditional execution step only — no questions, just install or skip based on what was already collected.

---

### Step 7 — Verify App State

- **Step:** Step 7
- **Observation:** Screenshots taken here for state verification are slow. `adb shell uiautomator dump` provides the same information faster without image transfer.
- **Suggested fix:** Use uiautomator dump as the primary state check; screenshot is still useful as formal evidence (pre-session.png) but should not be required just to confirm which screen is active.

---

### Step 8 — Execute Test Steps

- **Step:** Step 8
- **Observation 1:** Mechanical interaction steps (tap, type, wait, screenshot-for-evidence) have no agent-level thinking requirement. Running them in the main agent wastes context and slows execution.
- **Suggested fix 1:** Delegate all tap/type/wait/screenshot sequences to a sub-agent using a low-thinking model (Haiku or equivalent). The main agent defines the script; the sub-agent executes it and returns results.
- **Observation 2:** Screenshots used to determine coordinates for tapping are much slower than `adb shell uiautomator dump` + Python bounds parsing. Each screenshot requires image transfer and visual analysis.
- **Suggested fix 2:** Make uiautomator dump + Python bounds parsing the DEFAULT strategy for coordinate discovery. Reserve screenshots for official step evidence only (before/after). Add this guidance explicitly to the step instructions.

---

### Step 8b — Record Flow Script

- **Step:** Step 8b
- **Observation:** 
- **Suggested fix:** 

---

### Step 9 — Evidence Capture

- **Step:** Step 9
- **Observation:** 
- **Suggested fix:** 

---

### Step 10 — Write Test Report

- **Step:** Step 10
- **Observation:** 
- **Suggested fix:** 

---

### Step 11 — Present Summary

- **Step:** Step 11
- **Observation:** 
- **Suggested fix:** 

---

## General Skill Feedback

_Notes that don't fit a specific step — overall flow, tone, verbosity, missing guidance, etc._

- **Stale `.claude/skills/` symlink:** The `.claude/skills/android-emulator-qa` copy loaded in this session had the OLD 11-step SKILL.md, not the updated 13-step version from `skills-engineering/`. Steps 2b and 8b were missing. The skill ran correctly only because the skill body was also in the system-reminder from prior context. Fix: ensure the `.claude/skills/` symlink points to the live `skills-engineering/` source, or add a deployment step to the skill update workflow.
- **uiautomator dump is the right DOM tool:** For Flutter apps, uiautomator dump + Python bounds parsing reliably extracts EditText and Button coordinates (even though Flutter's tree is sparse). Screenshots should be evidence artifacts, not navigation tools.

---

### General (continued)

- **Write step results immediately:** As soon as each step completes, write Pass/Fail/Partial/N/A directly into the report file. Do not accumulate results in memory and write all at once at Step 10 — context can be lost mid-session (especially in long runs or crashes). Suggested approach: open/create the report file during Step 3 (Compose Testing Script) with empty result rows, then edit-in-place after each step.
- **UI hierarchy library idea (raised mid-session):** User suggests doing a one-time pass through all screens to dump and save their uiautomator XML/coordinate map as a persistent local file library. This would eliminate re-analysis for every run. See response below in Post-Session Patch Plan.

---

## Post-Session Patch Plan

_Filled after testing is complete. List what needs to change in SKILL.md and references._

| File | Section | Change Needed |
|------|---------|---------------|
| SKILL.md | New section before Step 1 | Add upfront AskUserQuestion block to collect APK path, install preference, credential source, device serial before any step |
| SKILL.md | Step 5 | Change to "read from pre-confirmed credential file" — no user question at this step |
| SKILL.md | Step 6 | Change to conditional install only — no mid-run question; use value collected upfront |
| SKILL.md | Step 7 | Add note: use uiautomator dump as primary state check; screenshot = evidence artifact only |
| SKILL.md | Step 8 | Add guidance: delegate tap/type/wait/screenshot sequences to Haiku sub-agent; use uiautomator dump for coordinate discovery; screenshots = evidence only |
| SKILL.md | Step 10 | Add guidance: create report file at start of Step 3 with empty rows; write each result immediately after execution |
| references/flutter-notes.md | UI Tree Limitations | Expand: Flutter Switch widgets DO appear as `android.widget.Switch` with checkable/checked attributes — use uiautomator dump to verify toggle state instead of screenshots |
| SKILL.md or new reference | UI Screen Map | Add concept of a persistent UI coordinate map per screen (see below) |
