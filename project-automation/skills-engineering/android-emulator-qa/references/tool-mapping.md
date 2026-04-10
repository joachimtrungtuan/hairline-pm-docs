# Tool Mapping: MCP ↔ Raw ADB

Use this table to select the right command based on your platform (MCP mode vs raw ADB mode).

## Detection Rule

- **MCP mode**: `get_screenshot`, `get_uilayout`, `execute_adb_command` tools are available
- **Codex built-in**: "Test Android Apps" skill is available in the sidebar
- **Raw ADB mode**: Neither above — use Bash with ADB commands directly

## Mapping Table

| Action | MCP Tool | Raw ADB Command |
|--------|----------|-----------------|
| List devices | `get_packages()` | `adb devices` |
| Launch app | `execute_adb_command("shell am start -n <pkg>/<activity>")` | `adb shell am start -n <pkg>/<activity>` |
| Force stop app | `execute_adb_command("shell am force-stop <pkg>")` | `adb shell am force-stop <pkg>` |
| Tap | `execute_adb_command("shell input tap <x> <y>")` | `adb shell input tap <x> <y>` |
| Swipe | `execute_adb_command("shell input swipe <x1> <y1> <x2> <y2> <ms>")` | `adb shell input swipe <x1> <y1> <x2> <y2> <ms>` |
| Type text | `execute_adb_command("shell input text \"<text>\"")` | `adb shell input text "<text>"` |
| Back key | `execute_adb_command("shell input keyevent 4")` | `adb shell input keyevent 4` |
| Home key | `execute_adb_command("shell input keyevent 3")` | `adb shell input keyevent 3` |
| Enter key | `execute_adb_command("shell input keyevent 66")` | `adb shell input keyevent 66` |
| Screenshot | `get_screenshot()` | `adb exec-out screencap -p > screen.png` |
| UI tree | `get_uilayout()` | `adb exec-out uiautomator dump /dev/tty` |
| Logcat snapshot | `execute_adb_command("logcat -d")` | `adb logcat -d` |
| Clear logcat | `execute_adb_command("logcat -c")` | `adb logcat -c` |
| Uninstall app | `execute_adb_command("uninstall <package>")` | `adb uninstall <package>` |
| Install APK | `execute_adb_command("install <path>.apk")` | `adb install <path>.apk` |
| Push file | `execute_adb_command("push <local> <remote>")` | `adb push <local> <remote>` |
| Pull file | `execute_adb_command("pull <remote> <local>")` | `adb pull <remote> <local>` |
| Screen size | `execute_adb_command("shell wm size")` | `adb shell wm size` |
| List packages | `get_packages()` | `adb shell pm list packages` |

## Notes

- In MCP mode, `execute_adb_command()` takes the command WITHOUT the leading `adb ` prefix
- `get_screenshot()` returns base64-encoded PNG — save to file if needed for reporting
- `get_uilayout()` returns XML — for Flutter apps, the tree is sparse; prefer coordinate-based interaction
- For text with special characters, use the clipboard workaround described in `references/adb-commands.md`

## Flutter-Specific Tool Notes

| Scenario | Preferred Approach |
|----------|--------------------|
| UI is sparse / no text nodes | Screenshot → coordinate analysis → `input tap` |
| `image_picker` dialog | Push test image to `/sdcard/Pictures/` first, then interact with native picker |
| Payment form (flutter_stripe) | Use test card numbers from staging config; interact via coordinates |
| App crash | Immediately run logcat → `execute_adb_command("logcat -d")` or `adb logcat -d` |
