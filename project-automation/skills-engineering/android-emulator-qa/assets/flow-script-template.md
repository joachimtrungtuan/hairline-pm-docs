---
flow-id: {kebab-case-name}
flow-name: {Human-Readable Name}
aliases: [{alias1}, {alias2}]
recorded: YYYY-MM-DD
last-tested: YYYY-MM-DD
status: stable
---

# Flow: {Human-Readable Flow Name}

## Preconditions

- App state: {e.g., logged out / logged in as patient / fresh install}
- Role: {patient / provider / admin}
- Required data: {any pre-existing data needed}
- Test account: {role — credentials loaded at runtime from testing-credentials/}

## Steps

| # | Screen | Action | Element Description | Coordinates | Expected Result | Status |
|---|--------|--------|---------------------|-------------|-----------------|--------|
| 1 | {screen name} | {action description} | {visible label, role, and position on screen} | ({x}, {y}) | {expected UI response} | stable |

**Element Description:** write what a human would say — the element's visible label, role, and position on screen. Required for re-identification if coordinates shift.

**Coordinates:** the actual pixel coordinates used during the recording session. Both columns always required.

## Test Data Used
- Step {N}: {field} — dataset: {dataset-id}

## Notes

- {Coordinate caveats — e.g., "Step 3 Y-coordinate shifts when top banner is visible"}
- {Flutter/WebView notes — e.g., "Step 7 is inside a Stripe WebView; coordinates are screen-absolute"}

---

**Step Status Reference**

| Value | Meaning |
|-------|---------|
| `stable` | Verified in last test run — coordinates and expected result confirmed accurate |
| `stale` | Element moved or changed since last run — coordinate needs re-verification before trusting |
| `unverified` | Recorded from PRD or first-draft but not yet tested against a real build |
