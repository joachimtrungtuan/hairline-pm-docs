---
name: android-flow-register
description: Interactively record a multi-screen Hairline app testing flow through a live guided session on the Android emulator/device, or update an existing flow when steps have changed. The user instructs each step in real time; the agent executes, captures state, and waits for the next instruction. On completion, writes the flow definition file and updates the flow index. Triggers on: "record this flow", "register a new flow", "add this flow to the registry", "flow not found — register it", "update this flow", "re-record [flow name]", "the flow steps have changed".
---

# Android Flow Register

Records or updates Hairline app testing flows through a live, user-guided interactive session on the Android emulator/device. The user instructs each action; the agent executes, captures state, and waits. Coordinates and element descriptions are recorded in real time from actual device interaction.

## Step 0: Upfront Input Collection

Ask ALL of the following before touching the device.

**1. Flow name?** (how it will appear in the index — human-readable)

**2. Aliases?** (other names or phrases a user might say to look this up — e.g., "login", "sign in", "auth" for a login flow; list as many as relevant)

**3. Trigger type?**
- `new` — recording a flow for the first time
- `update` — updating specific steps after a discrepancy (specify: which steps changed and why)

**4. Starting state?**
- App state before step 1 (e.g., "app is at login screen", "logged in as patient, at home screen")
- Role and test account to use

**5. First action?**
- User provides the very first instruction: what to tap, type, or swipe to begin

Do not interact with the device until all five items are resolved.

---

## Session Init

1. Detect platform (MCP / Codex / Raw ADB) — see `android-emulator-qa/references/tool-mapping.md`
2. Verify device connected
3. APK check (install if needed — Bash only for `adb install`)
4. Launch app and navigate to the declared starting state

---

## The Interactive Recording Loop

Repeat this loop until the user says **"done"** or **"complete"**.

### Each iteration:

**1. Receive user instruction**

Accept:
- `"tap [element description]"` — e.g., "tap the Sign In button"
- `"type [value]"` — e.g., "type test@email.com in the email field"
- `"type [mock/random/generate X]"` — e.g., "type a valid email" → see Test Data below
- `"swipe [direction]"` — e.g., "swipe up on the list"
- `"press back"` / `"press home"` / `"press enter"`
- `"wait"` — observe only; agent takes screenshot + UI hierarchy, no action
- `"done"` / `"complete"` → exit loop, proceed to Write Flow

**2. Capture pre-action state**

Take screenshot + retrieve UI hierarchy (`get_uilayout` in MCP; `uiautomator dump` in raw ADB).

Use both to:
- Locate the target element: match visual position with hierarchy node (text, content-desc, resource-id)
- Note the current screen name (infer from visible title, navigation bar, or prominent content)

**3. Resolve the action target**

- **Element clearly identified:** proceed
- **Ambiguous or multiple candidates:** show the screenshot and list candidates with their coordinates; ask the user to confirm which one before executing

**4. Execute**

Run the action using the appropriate tool — see `android-emulator-qa/references/tool-mapping.md`.

**5. Capture post-action state**

- Wait 1–2s for Flutter transition
- Take screenshot
- Retrieve UI hierarchy

**6. Report to user**

Present:
- Post-action screenshot
- Inferred screen name
- Key visible interactive elements (brief list — enough to orient the user)
- Preview of the step just recorded

Example:
```
Step 3 recorded:
  Screen: "Login"
  Action: Tap "Sign In" button
  Element: Primary CTA, bottom-center of screen
  Coordinates: (540, 1680)
  Observed result: Navigated to Home screen

Now on: Home screen
Visible elements: "Create Inquiry" FAB (bottom-right), bottom nav bar, patient name in header

What's next? (or type "done" to finish)
```

**7. Wait — do not auto-advance**

The agent never decides the next step. Always wait for the user's next instruction.

---

## Test Data During Recording

**Explicit value** (user says "type test@hairline.com"):
- Use the value exactly as given
- Propose to add it to `android-emulator-qa/references/datasets.json` as a dataset entry scoped to this screen
- Wait for user confirmation before writing

**Generated/mock value** (user says "type a valid email", "generate a phone number"):
- Propose a specific value (e.g., "tester_001@hairline-test.com")
- Show the proposal; wait for confirmation or amendment
- On confirmation: use the value and record it to `datasets.json`

**File input** (user says "select a hair photo", "choose a passport image"):
- Use the appropriate file from `android-emulator-qa/assets/`
- Push to device before the step: `adb push <local_path> <device_path>`
- Record both `local_path` and `device_path` in `datasets.json` and in the flow step's Notes

---

## Writing the Flow (on "done")

### 1. Write the individual flow file

Save to `android-flow-test/references/flows/{flow-id}.md`, using `android-emulator-qa/assets/flow-script-template.md` as the template. Fill in all frontmatter fields (`flow-id`, `flow-name`, `aliases`, `recorded`, `last-tested`, `status`) and populate the Steps table, Test Data Used, and Notes sections from the session just recorded.

### 2. Update the flow index

Append or update the entry in `android-flow-test/references/flow-index.md`:

```
| {Flow Name} | {alias1}, {alias2} | flows/{flow-id}.md | stable | YYYY-MM-DD |
```

If updating an existing entry: find it by flow-id and replace the status and date in place.

### 3. Confirm to user

Tell the user:
- Flow is registered under the name and aliases provided
- File written to `android-flow-test/references/flows/{flow-id}.md`
- Index entry updated in `android-flow-test/references/flow-index.md`
- "You can now run this flow with `android-flow-test`."

---

## Updating an Existing Flow (update trigger)

1. Load the existing flow file from `android-flow-test/references/flows/`
2. Show the user the current step definitions for the affected steps
3. Re-run the interactive recording loop for those steps only
4. Update the flow file: correct coordinates/descriptions, bump `last-tested`, update per-step `Status`
5. Set overall `status: stable` if all affected steps re-verified; otherwise `needs-review`
6. Update the flow-index.md entry's status and date

---

## Screenshot Cleanup

After writing the flow and confirming with the user:
1. Ask: "Delete all screenshots captured during this recording session from `local-docs/reports/`?"
2. On user confirmation: delete the session screenshot folder

---

## References

- `android-emulator-qa/references/tool-mapping.md` — MCP ↔ ADB command table; read during Session Init and throughout the recording loop for command selection
- `android-emulator-qa/references/adb-commands.md` — Raw ADB command reference; read only in Raw ADB mode
- `android-emulator-qa/references/flutter-notes.md` — Flutter interaction caveats; read when encountering Flutter-specific interaction issues during the recording loop
- `android-emulator-qa/assets/flow-script-template.md` — Flow file format template; read when writing the individual flow file (Writing the Flow, Step 1)
- `android-flow-test/references/flow-index.md` — Registered flow index; read when updating the index after recording (Writing the Flow, Step 2)
- `android-emulator-qa/references/datasets.json` — Test data catalogue; read during the recording loop when the user provides or generates test data values
- Test credentials: `local-docs/testing-plans/testing-credentials/`
