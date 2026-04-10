---
name: android-emulator-qa
description: Test a SINGLE SCREEN of the Hairline Flutter Android app on an emulator or physical device. Use for: (1) verifying UI elements and interactions on one specific screen, (2) reproducing a bug on a known screen, (3) form validation and input testing on one screen, (4) visual/layout checks of a specific screen. Scope is one navigation destination — tabs within that screen are in-scope; navigating away to a different screen is out of scope. For multi-screen flows, use android-flow-test instead. Triggers on: "test the [X] screen", "check [screen name]", "reproduce bug on [screen]", "verify form on [screen]", "does [screen] show [X]", "screenshot the [screen]", "test this UI", "check this view".
---

# Android Emulator QA — Single Screen

Tests one navigation destination of the Hairline Flutter app. Navigate to the target screen, then test interactions and UI state on that screen only. Navigating to a new screen is out of scope.

## Step 0: Upfront Input Collection

Ask ALL of the following before any device interaction. Do not start until all answers are resolved.

**1. Which screen?** (name, description, or how to navigate there)

**2. Scenario type?**
- `happy-path` — normal valid interaction, expect correct behavior
- `error-state` — trigger validation errors, empty states, warning banners
- `edge-case` — boundary values in inputs, unusual but valid data
- `visual-check` — layout and element presence only, no interaction
- `negative-flow` — attempt invalid operations (submit empty form, tap disabled button, etc.)

**3. App state required?**
- Which role? (patient / provider / admin)
- Fresh install, or existing account with data?
- Any specific data that must exist? (e.g., existing inquiry ID, accepted quote)

**4. Test data:** run the test data selection workflow (see Test Data Management) before proceeding. Collect all data decisions here — do not ask mid-test.

---

## Platform Detection

Detect once. Use one mode for the entire session. Read [tool-mapping.md](references/tool-mapping.md) for the full command table.

| Check | Mode |
|-------|------|
| `get_screenshot`, `get_uilayout`, `execute_adb_command` available | **MCP** |
| Codex "Test Android Apps" built-in available | **Codex built-in** |
| Neither | **Raw ADB** — Bash; see [adb-commands.md](references/adb-commands.md) |

---

## Test Data Management

Test data is stored in [datasets.json](references/datasets.json). Each entry is scoped to a screen + scenario type.

### Selection workflow (run during Step 0)

1. Read `references/datasets.json`
2. Filter entries by target screen and scenario type
3. Present to user:
   - **Matches found:** list by name + description — ask to reuse an existing one, or create new for variety
   - **No matches:** offer to add a new dataset (see below)

### Adding a new dataset

1. Ask what inputs the screen requires (or read the relevant FR at `local-docs/project-requirements/functional-requirements/`)
2. Propose a payload that fits the scenario type — for error/edge cases, propose data that deliberately triggers the condition
3. For fields requiring files: use files from `assets/` and note the `device_path` where they must be pushed
4. Wait for user confirmation, then write the entry to `references/datasets.json`

### Dataset entry format

```json
{
  "id": "inquiry-form-happy-001",
  "screen": "Inquiry Creation Form",
  "scenario": "happy-path",
  "description": "Valid inquiry with hair photo",
  "text_inputs": {
    "notes": "Looking for FUE transplant, 2000 grafts"
  },
  "file_inputs": [
    {
      "field": "hair_photos",
      "local_path": "assets/sample-hair-photo.jpg",
      "device_path": "/sdcard/Pictures/sample-hair-photo.jpg"
    }
  ]
}
```

### Pushing files to device

Before any step that uses a file input, push the file first:
- MCP: `execute_adb_command("push <local_path> <device_path>")`
- Raw ADB: `adb push <local_path> <device_path>`

Confirm the push succeeded before proceeding.

---

## Hard Rules

- **Never modify app code or backend** — observation only
- Screenshot BEFORE and AFTER every interaction step
- On crash → capture logcat immediately → stop → report (do not continue remaining steps)
- Save screenshots to `local-docs/reports/YYYY-MM-DD/android-qa-{session-id}/`
- Save test report to `local-docs/reports/YYYY-MM-DD/android-qa-{slug}.md`
- **Never hard-code credentials** — read from `local-docs/testing-plans/testing-credentials/` only
- **Redact all sensitive data with `[REDACTED]`** in reports
- One screen per run

---

## Execution

### Step 1: Verify device

Confirm device connected: `adb devices` (Raw ADB) or `get_packages()` (MCP). No device found → stop and report.

### Step 2: APK check

1. Check if installed: `adb shell pm list packages com.samasu.hairline`
2. **Not installed** → ask for APK path → install → confirm `Success`
3. **Installed, new version** → uninstall → install → confirm `Success`
4. **Same version** → skip

APK install is **Bash only** — `adb install` is a host-side command; MCP cannot run it.

### Step 3: Push file inputs

For each `file_input` in the selected dataset, push to device now — before launching the app.

### Step 4: Launch and navigate to screen

1. Launch: `am start -n com.samasu.hairline/<main-activity>`
2. Screenshot → `pre-session.png`
3. Navigate to the target screen using the minimum required steps
4. Screenshot → `screen-ready.png`
5. Confirm the correct screen is visible before starting test steps

### Step 5: Execute test steps

For each action:
1. Screenshot BEFORE → `step-{N}-before.png`
2. Execute action — see [tool-mapping.md](references/tool-mapping.md); see [flutter-notes.md](references/flutter-notes.md) for Flutter caveats
3. Wait 1–2s for Flutter transitions
4. Screenshot AFTER → `step-{N}-after.png`
5. Record: **Pass** / **Fail** / **Partial** / **N/A** with notes

On crash → go to Step 6 immediately.

### Step 6: Capture evidence

1. Screenshot → `session-end.png`
2. Capture logcat (always, not just on crash): `adb logcat -d` filtered to `com.samasu.hairline`

### Step 7: Write report

Copy `assets/test-report-template.md` → save to `local-docs/reports/YYYY-MM-DD/android-qa-{slug}.md`. Fill in all sections.

Run the quality checklist in [flutter-notes.md](references/flutter-notes.md) before finalizing.

### Step 8: Screenshot cleanup

After the report is written and confirmed:
1. Ask: "Delete working screenshots from `local-docs/reports/YYYY-MM-DD/android-qa-{session-id}/`?"
2. On user confirmation: delete the session screenshot folder
3. Keep only the report `.md` file

---

## References

- [tool-mapping.md](references/tool-mapping.md) — MCP ↔ ADB command table
- [adb-commands.md](references/adb-commands.md) — Raw ADB command reference
- [flutter-notes.md](references/flutter-notes.md) — Flutter interaction caveats and quality checklist
- [mcp-setup.md](references/mcp-setup.md) — MCP setup instructions; read only when setting up the MCP server for the first time
- [datasets.json](references/datasets.json) — Test data catalogue
- [flow-script-template.md](assets/flow-script-template.md) — Flow file format template; used by `android-flow-register` when writing individual flow files
- Test credentials: `local-docs/testing-plans/testing-credentials/`
