# MCP Server Setup: android-mcp-server

## Prerequisites

- Python 3.11+
- `uv` package manager (`pip install uv` or `brew install uv`)
- ADB installed in PATH — `brew install android-platform-tools`, verify: `adb version`
- Android emulator running OR physical device with USB debugging enabled

## Installation (android-mcp-server — PRIMARY)

```bash
# Clone to global tools directory
mkdir -p ~/tools
git clone https://github.com/minhalvp/android-mcp-server.git ~/tools/android-mcp-server

# Install as a global uv tool (updatable via `uv tool upgrade --all`)
uv tool install ~/tools/android-mcp-server

# Verify
android-mcp-server --help 2>/dev/null || echo "installed"
adb devices
```

## Post-Install Security Check (MANDATORY)

Run before first use and after any update:

```bash
cd ~/tools/android-mcp-server
uv run pip-audit
```

If `pip-audit` reports any CVEs, run `uv tool upgrade android-mcp` and re-audit before use.

## Updating

```bash
# Pull latest source
cd ~/tools/android-mcp-server && git pull

# Reinstall the global tool from updated source
uv tool install ~/tools/android-mcp-server --force

# Re-audit after update
uv run pip-audit
```

Alternatively, upgrade all global uv tools at once (includes this server):
```bash
uv tool upgrade --all
```

## Platform MCP Config

The command is simply `android-mcp-server` with no arguments.

### Claude Code (global — `~/.claude.json`)
```bash
claude mcp add android-emulator --scope user -- android-mcp-server
```

### Codex (global — `~/.codex/config.toml`)
```toml
[mcp_servers.android-emulator]
command = "android-mcp-server"
args = []
```

### Antigravity (global — `~/.gemini/antigravity/mcp_config.json`)
```json
"android-emulator": {
  "command": "android-mcp-server",
  "args": [],
  "env": {}
}
```

## Available MCP Tools (android-mcp-server)

| Tool | Description |
|------|-------------|
| `get_packages()` | List installed packages on connected device |
| `get_screenshot()` | Capture current screen as base64 PNG |
| `get_uilayout()` | Dump UI hierarchy as XML |
| `execute_adb_command(command)` | Run any ADB shell command |

## Fallback: replicant-mcp (Node.js)

Use if android-mcp-server is unavailable. Blocks dangerous commands (`rm -rf /`, `reboot`, `su`).

```bash
npm install -g replicant-mcp
npm audit  # mandatory security check before use
```

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `adb: no devices` | Start emulator or enable USB debugging; run `adb kill-server && adb start-server` |
| `android-mcp-server: command not found` | Run `uv tool install ~/tools/android-mcp-server`; ensure `~/.local/bin` is in PATH |
| MCP server not connecting | Verify `android-mcp-server` is in PATH: `which android-mcp-server` |
| CVEs found after update | Run `uv tool upgrade android-mcp --force` and re-audit |
