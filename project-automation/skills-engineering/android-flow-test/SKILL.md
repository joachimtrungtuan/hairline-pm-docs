---
name: android-flow-test
description: Run a named multi-screen Hairline app testing flow end-to-end on an Android emulator or device. Use when the user wants to test a complete user journey across multiple screens — e.g., "test the inquiry creation flow", "run the patient onboarding flow", "test the full login-to-inquiry flow", "test the quote acceptance journey". Looks up the flow in a registered index — if not found, halts and directs to android-flow-register first. Triggers on: "test the [X] flow", "run the [X] flow", "end-to-end app test", "test complete journey", "multi-screen test", "test [user journey] on the app".
---

# Android Flow Test

Executes multi-screen Hairline app testing flows end-to-end on the Android emulator/device. Applies `android-emulator-qa` interaction patterns at each step. Flow definitions live in `references/flows/` and are indexed in `references/flow-index.md`.

## Step 0: Upfront Input Collection

Ask ALL of the following before any device interaction.

**1. Flow name?** (what the user calls it — can be vague, will be matched below)

**2. Scenario variant?**
- `happy-path` — standard expected-success journey
- `edge-case` — specify which edge scenario
- `error-path` — specify which error condition to trigger
- `negative` — test invalid operations within the flow

**3. Starting state?**
- Does prerequisite data already exist? If yes, provide relevant IDs
- Or create everything from scratch?

**4. Per-step overrides?** Or use the defaults defined in the flow file?

**5. Test data:** after confirming the flow, check `android-emulator-qa/references/datasets.json` for datasets matching each step's screen + scenario. Collect all data decisions upfront — do not interrupt execution to ask.

---

## Flow Lookup with Fuzzy Matching

Read `references/flow-index.md`. Search for the user's query against both the **Flow Name** and **Aliases** columns.

**Multiple candidates found** — present the list and ask the user to confirm:
```
I found these flows matching "[user's query]":

1. Patient Login — aliases: "login", "sign in", "auth" [stable · 2026-04-10]
2. Patient Login + Onboarding — aliases: "onboarding", "first login" [needs-review · 2026-03-28]

Which one would you like to run? (Enter number, or "none of these")
```
Wait for user selection before loading anything.

**Exact or single match found** — still confirm once:
```
Found: "Patient Login" (aliases: login, sign in, auth) — last recorded 2026-04-10, status: stable.
Run this flow? (yes / no)
```

**No match found:**
- Stop. Tell the user: "No flow matching '[name]' is registered."
- Instruct: "Run `android-flow-register` to record it first, then come back."

**After confirmation:** load the flow file from `references/flows/{flow-id}.md`. Check `recorded` and `status`:
- `needs-review` or recorded > 4 weeks ago → warn the user; ask whether to proceed or update first via `android-flow-register`

---

## Platform Detection

Detect once. Use one mode for the entire session. See `android-emulator-qa/references/tool-mapping.md` for commands.

---

## Execution

### Session init

1. Verify device connected
2. APK check (install/update if needed — Bash only for `adb install`)
3. Push any file inputs needed by the flow to the device before launching
4. Launch app to the starting state defined in the flow file

### Step-by-step execution

For each step in the flow file:

1. Screenshot BEFORE → `step-{N}-before.png`
2. **`stable` steps:** use the recorded coordinates directly
3. **`stale` or `unverified` steps:** take screenshot + UI hierarchy first; verify the element is at the recorded position before tapping; if the position has shifted, note the discrepancy
4. Execute the action — see `android-emulator-qa/references/tool-mapping.md`; see `android-emulator-qa/references/flutter-notes.md` for Flutter caveats
5. Wait 1–2s for Flutter transition
6. Screenshot AFTER → `step-{N}-after.png`
7. Record: **Pass** / **Fail** / **Partial** / **N/A**

**On discrepancy detected** (coordinate wrong, screen shows unexpected content, step fails in an unexpected way):
1. Pause execution immediately
2. Report to user: what the flow file expected vs what actually happened, with screenshots
3. Ask: continue with a manual correction this session, or trigger `android-flow-register` to update the flow definition?
4. Wait for decision before continuing

**On crash:** capture logcat immediately, mark remaining steps N/A, stop.

### Capture logcat

After all steps complete: `adb logcat -d` filtered to `com.samasu.hairline`.

### End-of-flow summary

```
## Flow Test Summary — [Flow Name]

**Scenario:** [variant]
**Overall result:** PASS / PARTIAL / FAIL

| # | Screen            | Action                   | Result  | Screenshot       |
|---|-------------------|--------------------------|---------|------------------|
| 1 | Login             | Enter credentials + tap  | Pass    | step-1-after.png |
| 2 | Home              | Tap "Create Inquiry"     | Pass    | step-2-after.png |
| 3 | Inquiry Form      | Fill + submit            | Partial | step-3-after.png |

### Issues Found
- Step 3: [description]

### Logcat Anomalies
- [Any app errors]
```

### Screenshot cleanup

After the summary is confirmed:
1. Ask: "Delete working screenshots from the session folder in `local-docs/reports/`?"
2. On user confirmation: delete the session screenshot folder
3. Keep only the report `.md` file

---

## References

- [flow-index.md](references/flow-index.md) — Registered flow index (name, aliases, file paths, status); read during Flow Lookup
- `references/flows/` — Individual flow definition files; load the matched flow file after user confirmation
- `android-emulator-qa/references/tool-mapping.md` — MCP ↔ ADB command table; read during Platform Detection
- `android-emulator-qa/references/adb-commands.md` — Raw ADB command reference; read only in Raw ADB mode
- `android-emulator-qa/references/flutter-notes.md` — Flutter interaction caveats and quality checklist; read before execution and before finalizing the summary
- `android-emulator-qa/references/datasets.json` — Test data catalogue; read during Step 0 test data coordination
- Test credentials: `local-docs/testing-plans/testing-credentials/`
