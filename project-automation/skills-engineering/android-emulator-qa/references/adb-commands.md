# ADB Command Reference

Raw ADB commands for use in Codex / raw ADB fallback mode. Each command includes a working example.

## Device Management

```bash
# List connected devices/emulators
adb devices

# Target a specific device (if multiple connected)
adb -s emulator-5554 <command>

# Restart ADB server
adb kill-server && adb start-server
```

## App Management

```bash
# Install APK (uninstall first — never use adb install -r; see flutter-notes.md)
adb uninstall com.samasu.hairline
adb install build/app/outputs/flutter-apk/app-release.apk

# Launch app by package and activity
adb shell am start -n com.samasu.hairline/.MainActivity

# Force stop app
adb shell am force-stop com.samasu.hairline

# List installed packages
adb shell pm list packages | grep hairline
```

## Input Simulation

```bash
# Tap at coordinates
adb shell input tap 540 960

# Swipe (x1 y1 x2 y2 duration_ms)
adb shell input swipe 540 1200 540 600 300

# Type text (URL-encode spaces as %s; avoid special chars)
adb shell input text "testuser%40email.com"

# Key events
adb shell input keyevent 4    # Back
adb shell input keyevent 3    # Home
adb shell input keyevent 66   # Enter
adb shell input keyevent 67   # Delete/Backspace
adb shell input keyevent 111  # Escape

# Long press
adb shell input swipe 540 960 540 960 1000
```

## Screenshot & Screen Recording

```bash
# Capture screenshot to local file
adb exec-out screencap -p > screen.png

# Capture with timestamp
adb exec-out screencap -p > "screen_$(date +%Y%m%d_%H%M%S).png"

# Record screen (30 sec max by default)
adb shell screenrecord /sdcard/demo.mp4
adb pull /sdcard/demo.mp4 .
```

## UI Inspection

```bash
# Dump UI hierarchy to stdout (useful for piping)
adb exec-out uiautomator dump /dev/tty

# Dump to file on device, then pull
adb shell uiautomator dump /sdcard/ui.xml
adb pull /sdcard/ui.xml .

# Get window dimensions
adb shell wm size
```

## File Operations

```bash
# Push file to device (e.g., test image to gallery)
adb push test_image.jpg /sdcard/Pictures/

# Pull file from device
adb pull /sdcard/Pictures/test_image.jpg .

# List directory on device
adb shell ls /sdcard/

# Delete file on device
adb shell rm /sdcard/test_image.jpg
```

## Logcat

```bash
# Dump current log (snapshot)
adb logcat -d

# Dump and filter by tag
adb logcat -d -s FlutterError

# Clear log buffer
adb logcat -c

# Stream log with filter (Ctrl+C to stop)
adb logcat | grep -i error

# Save logcat to file
adb logcat -d > logcat_$(date +%Y%m%d_%H%M%S).txt
```

## Flutter-Specific

```bash
# Build release APK
flutter build apk --release

# Install release APK (uninstall first — never use adb install -r; see flutter-notes.md)
adb uninstall com.samasu.hairline
adb install build/app/outputs/flutter-apk/app-release.apk

# Build + install (uninstall first)
flutter build apk --release && adb uninstall com.samasu.hairline && adb install build/app/outputs/flutter-apk/app-release.apk

# Flutter log (structured Flutter output)
flutter logs
```

## Clipboard & Text Input Tips

For text with special characters (spaces, @, #, etc.), use clipboard method:
```bash
# Set clipboard content, then paste
adb shell am broadcast -a clipper.set -e text "Hello World"
adb shell input keyevent 279  # KEYCODE_PASTE (may not work on all devices)

# Alternative: use input text with URL encoding
# Space = %s, @ = need workaround via clipboard
```
