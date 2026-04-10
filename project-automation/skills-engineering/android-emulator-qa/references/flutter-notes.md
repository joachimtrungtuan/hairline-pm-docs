# Flutter & Android Interaction Notes

## APK Installation

The developer sends a new `.apk` for each build. Always uninstall before installing the new one — never use `adb install -r`. Clean install prevents cached data from contaminating the test session.

APK installation is **always Bash only** — it is a host-side ADB command. The MCP server's `execute_adb_command` only runs device-side shell commands and cannot run `adb install`. See `references/tool-mapping.md`.

## UI Tree Limitations

`uiautomator dump` returns a sparse tree for Flutter apps — most elements have empty `text` and `content-desc`. **Coordinate-based interaction is the primary strategy**: take a screenshot, analyze visually, derive (x, y) coordinates for taps.

## Image Picker / Image Cropper

`image_picker` and `image_cropper` invoke native Android system pickers, which are visible to ADB. Push a test image to `/sdcard/Pictures/` before triggering the picker:

```bash
adb push /path/to/test-image.jpg /sdcard/Pictures/test-image.jpg
```

## Payment Screens (flutter_stripe)

The Stripe payment form renders as a WebView. Interact via screen-absolute coordinates — the WebView does not expose native accessibility nodes. Use test card numbers from the staging config.

## Error Handling

| Error | Recovery Action |
|-------|----------------|
| Device disconnect | `adb kill-server && adb start-server` → reconnect → resume from last completed step |
| App crash | Capture logcat immediately, mark remaining steps N/A, proceed to Step 6 (Capture evidence) |
| Screenshot fails | Continue with text-only record; note failure in report |
| Picker doesn't open | Push test image to `/sdcard/Pictures/` via ADB, retry |
| Empty UI tree | Fall back to screenshot + visual coordinate analysis |
| MCP tool unavailable mid-session | Switch to raw ADB for remaining steps, note in report |

## Quality Checklist (Before Finalizing Report)

- [ ] All steps have a result (Pass / Fail / Partial / N/A)
- [ ] Every Fail/Partial has a screenshot reference and notes
- [ ] Logcat captured for any crash or anomaly
- [ ] All screenshots are indexed in the report
- [ ] No raw credentials appear anywhere in the report
- [ ] Every defect has a severity assigned (Critical / Major / Minor / Cosmetic)
- [ ] Report path and screenshot directory path are correct
