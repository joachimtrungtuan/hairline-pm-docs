---
description: Execute bash commands to interact with Plane.so API for listing users, projects, modules, tags, work item types, stages, and creating work items.
---

## User Input

```text
$ARGUMENTS
```

**CRITICAL**: User specifies operation in prompt. If not provided, ask: "Please specify operation: list-users, list-projects, list-modules, list-tags, list-work-item-types, list-stages, or create-work-item"

## Prerequisites

1. **`.env` file**: `local-docs/task-creation/plane-api/.env` (copy from `.env.example` if missing)
2. **System Variables**: `local-docs/plane-config/samasu-system-variables.md` - **MUST** reference for alternative IDs when defaults not applicable
3. **Tools required**:
   - `python3` (Python 3.x) - **REQUIRED** for reliable JSON handling
   - `curl` - for API calls
   - `jq` (optional) - for response formatting
4. `PLANE_API_KEY` in `.env` (format: `plane_api_...`)

## Default Configuration Values

These values are used when creating tasks (from `samasu-system-variables.md`):

| Parameter | Value | Description |
|-----------|-------|-------------|
| `WORKSPACE_SLUG` | `samasu-digital` | Workspace identifier |
| `PROJECT_ID` | `ff2d96b2-0ab2-438b-b879-fbdaa078dbd6` | Default project UUID |
| `ASSIGNEE_ID` | `c5bb905a-57bc-4f08-aee0-32d69f8fec78` | Default assignee UUID |
| `STAGE_ID` | `b189d1d2-0d1d-40f9-9a22-7e4ea5f5976f` | Default state (Drafted) |
| `PRIORITY` | `medium` | Default priority |
| `ISSUE_TYPE_ID` | `ee71055e-0962-4d04-bab7-e434c1347d8d` | Default issue type |
| `BASE_URL` | `https://api.plane.so/api/v1` | Plane API base URL |

**CRITICAL**: If defaults not applicable, **MUST** reference `samasu-system-variables.md` for alternative IDs (team members, issue types, states, labels, priorities)

## Markdown Task Format

**CRITICAL**: Only format used. Tasks **MUST** follow this structure:

```markdown
## TASK_NAME_START
[FE+BE TASK] Task Name
## TASK_NAME_END

**Status**: Drafted

## TASK_DESCRIPTION_START
<h2>Overview</h2>
<p>Description text here...</p>
<h2>Reference</h2>
<ul>
<li><a href="...">Link text</a></li>
</ul>
<h2>Current Status</h2>
<ul>
<li>Status item 1</li>
</ul>
<h2>Expectation (Suggestion)</h2>
<p><strong>Note (Suggestion):</strong> ...</p>
<ul>
<li>Requirement 1</li>
</ul>
<h2>Acceptance Criteria</h2>
<ol>
<li>Criterion 1</li>
</ol>
## TASK_DESCRIPTION_END
```

**Prefixes**: `[FE+BE TASK]`, `[FE TASK]`, `[BE TASK]`, `[BUG]`, `[UX/UI TASK]` - **DO NOT** remove from task name.

**Status**: `Drafted`, `Confirmed`, `Added to Plane`

**CRITICAL**: The `TASK_DESCRIPTION_START/END` content must be valid HTML for Plane.so's `description_html` field:
- Use `<h2>` for section headers
- Use `<p>` for paragraphs
- Use `<ul>/<ol>` with `<li>` for lists
- Use `<a href="...">` for links
- Use `<strong>`, `<code>` for formatting

---

## Recommended Method: Python Script (Proven Approach)

This is the **proven, reliable method** for creating multiple tasks from a markdown file. It handles JSON escaping correctly and processes all tasks in a single execution.

### Step 1: Read the Markdown File

First, read the implementation tasks file to understand its contents:

```python
# Read the file
file_path = "/path/to/implementation-tasks-YYYY-MM-DD-XXX.md"
```

### Step 2: Execute the Python Script

Run this Python script from the `plane-api` directory:

```bash
cd "/Users/joachimtrungtuan/My Documents/Vân Tay Media/Products/Hairline/local-docs/task-creation/plane-api" && python3 << 'PYTHON_SCRIPT'
import json
import re
import subprocess

# =============================================================================
# CONFIGURATION - Update these values as needed
# =============================================================================
file_path = "/Users/joachimtrungtuan/My Documents/Vân Tay Media/Products/Hairline/local-docs/task-creation/YYYY-MM-DD/implementation-tasks-YYYY-MM-DD-XXX.md"

# API Configuration (from .env and samasu-system-variables.md)
PLANE_API_KEY = os.environ.get("PLANE_API_KEY", "")  # Load from .env — NEVER hardcode
WORKSPACE_SLUG = "samasu-digital"
BASE_URL = "https://api.plane.so/api/v1"
PROJECT_ID = "ff2d96b2-0ab2-438b-b879-fbdaa078dbd6"
ASSIGNEE_ID = "c5bb905a-57bc-4f08-aee0-32d69f8fec78"
STAGE_ID = "b189d1d2-0d1d-40f9-9a22-7e4ea5f5976f"
PRIORITY = "medium"
ISSUE_TYPE_ID = "ee71055e-0962-4d04-bab7-e434c1347d8d"

# =============================================================================
# SCRIPT LOGIC - Do not modify below unless necessary
# =============================================================================

# Read the markdown file
with open(file_path, 'r') as f:
    content = f.read()

# Extract tasks using regex pattern
# This pattern matches TASK_NAME_START/END and TASK_DESCRIPTION_START/END blocks
tasks = []
pattern = r"## TASK_NAME_START\n(.*?)\n## TASK_NAME_END[\s\S]*?## TASK_DESCRIPTION_START\n([\s\S]*?)\n## TASK_DESCRIPTION_END"

for match in re.finditer(pattern, content):
    name = match.group(1).strip()
    desc = match.group(2).strip()
    tasks.append({"name": name, "description": desc})

print(f"Found {len(tasks)} tasks to create\n")

# Create all tasks in Plane.so
results = []
for i, task in enumerate(tasks, 1):
    # Build the payload
    payload = {
        "name": task["name"],
        "description_html": task["description"],
        "project": PROJECT_ID,
        "assignees": [ASSIGNEE_ID],
        "state": STAGE_ID,
        "priority": PRIORITY,
        "issue_type": ISSUE_TYPE_ID,
    }
    
    # API endpoint
    url = f"{BASE_URL}/workspaces/{WORKSPACE_SLUG}/projects/{PROJECT_ID}/issues/"
    
    # Convert payload to JSON (Python handles escaping correctly)
    payload_json = json.dumps(payload)
    
    # Build curl command
    cmd = [
        "curl", "-s", "-X", "POST", url,
        "-H", f"X-API-Key: {PLANE_API_KEY}",
        "-H", "Content-Type: application/json",
        "-d", payload_json,
    ]
    
    # Execute curl
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    print(f"Task {i}: {task['name']}")
    
    if result.returncode == 0:
        try:
            resp = json.loads(result.stdout)
            if "id" in resp:
                print(f"✓ Created successfully! ID: {resp['id']}\n")
                results.append({"name": task["name"], "id": resp["id"], "status": "success"})
            else:
                print(f"✗ Error response: {result.stdout}\n")
                results.append({"name": task["name"], "status": "error", "response": result.stdout})
        except json.JSONDecodeError:
            print(f"✗ Invalid JSON response: {result.stdout}\n")
            results.append({"name": task["name"], "status": "error", "response": result.stdout})
    else:
        print(f"✗ Curl error: {result.stderr}\n")
        results.append({"name": task["name"], "status": "error", "error": result.stderr})

# Print summary
success_count = len([r for r in results if r.get("status") == "success"])
print(f"\n{'='*60}")
print(f"Summary: {success_count} of {len(tasks)} tasks created successfully")
print(f"{'='*60}")

# Print mapping table for reference
if success_count > 0:
    print("\nTask ID Mapping:")
    print("-" * 80)
    for r in results:
        if r.get("status") == "success":
            print(f"  {r['name'][:60]}...")
            print(f"    → ID: {r['id']}")
PYTHON_SCRIPT
```

### Why Python Instead of Bash?

1. **Reliable JSON Handling**: Python's `json.dumps()` correctly escapes special characters (quotes, newlines, HTML entities) that break bash string handling
2. **Multi-line HTML Support**: The task descriptions contain complex HTML that bash struggles to escape properly
3. **Better Error Handling**: Python provides clear error messages and can parse API responses
4. **Single Execution**: All tasks are created in one script run with progress tracking

---

## Agent Workflow for Creating Tasks

When a user asks to create tasks from a markdown file, follow these steps:

### 1. Read the Markdown File

```python
# Use the Read tool to get the file contents
Read(path="/path/to/implementation-tasks-YYYY-MM-DD-XXX.md")
```

### 2. Create a Todo List for Tracking

```python
TodoWrite(
    merge=False,
    todos=[
        {"id": "t1", "content": "Create Plane issues from implementation-tasks file", "status": "in_progress"}
    ]
)
```

### 3. Execute the Python Script

Use the Shell tool to run the Python script:

```python
Shell(
    command='cd "/Users/joachimtrungtuan/My Documents/Vân Tay Media/Products/Hairline/local-docs/task-creation/plane-api" && python3 << \'PYTHON_SCRIPT\'\n... (full script here) ...\nPYTHON_SCRIPT',
    description="Create Plane issues for all tasks",
    block_until_ms=600000  # 10 minutes for large task lists
)
```

### 4. Update Todo and Report Results

After successful execution, update the todo and report:
- Number of tasks created
- Task names and their Plane IDs
- Any errors encountered

---

## Alternative: Bash Setup (Legacy)

For simple operations or when Python is unavailable:

```bash
# Navigate to plane-api directory
cd "local-docs/task-creation/plane-api"

# Verify .env file exists
[ ! -f ".env" ] && { echo "ERROR: .env file not found."; exit 1; }

# Load environment variables
export $(grep -v '^#' .env | grep -v '^$' | xargs)
BASE_URL="${BASE_URL:-https://api.plane.so/api/v1}"

# Validate API key
[ -z "$PLANE_API_KEY" ] && { echo "ERROR: PLANE_API_KEY not set"; exit 1; }

# Default values
DEFAULT_PROJECT_ID="ff2d96b2-0ab2-438b-b879-fbdaa078dbd6"
DEFAULT_ASSIGNEE_ID="c5bb905a-57bc-4f08-aee0-32d69f8fec78"
DEFAULT_STAGE_ID="b189d1d2-0d1d-40f9-9a22-7e4ea5f5976f"
DEFAULT_PRIORITY="medium"
DEFAULT_ISSUE_TYPE_ID="ee71055e-0962-4d04-bab7-e434c1347d8d"
DEFAULT_WORKSPACE_SLUG="samasu-digital"
```

---

## API Operations Reference

### List Operations

| Operation | Endpoint | Example |
|-----------|----------|---------|
| List Users | `members/` | `GET /workspaces/{slug}/members/` |
| List Projects | `projects/` | `GET /workspaces/{slug}/projects/` |
| List Modules | `projects/{id}/modules/` | `GET /workspaces/{slug}/projects/{id}/modules/` |
| List Tags | `projects/{id}/labels/` | `GET /workspaces/{slug}/projects/{id}/labels/` |
| List Issue Types | `projects/{id}/issue-types/` | `GET /workspaces/{slug}/projects/{id}/issue-types/` |
| List States | `projects/{id}/states/` | `GET /workspaces/{slug}/projects/{id}/states/` |

### Create Issue API

```
POST /workspaces/{workspace_slug}/projects/{project_id}/issues/

Headers:
  X-API-Key: {api_key}
  Content-Type: application/json

Body:
{
  "name": "[FE TASK] Task Name",
  "description_html": "<h2>Overview</h2><p>...</p>",
  "project": "{project_id}",
  "assignees": ["{assignee_id}"],
  "state": "{state_id}",
  "priority": "medium",
  "issue_type": "{issue_type_id}"
}
```

**Response (201 Created)**:
```json
{
  "id": "uuid-of-created-issue",
  "name": "[FE TASK] Task Name",
  ...
}
```

---

## Error Handling

| Code | Meaning | Solution |
|------|---------|----------|
| 401 | Invalid/expired API key | Regenerate API key in Plane settings |
| 400 | Validation error | Check required fields and JSON format |
| 404 | Invalid workspace/project ID | Verify IDs in samasu-system-variables.md |
| 429 | Rate limit (60/min) | Wait for reset, check `X-RateLimit-Remaining` |
| 5xx | Server error | Retry after a few seconds |

---

## Troubleshooting

### "JSON parse error" when creating issues

**Cause**: Special characters in task description not properly escaped

**Solution**: Use the Python script method which handles JSON escaping correctly

### Tasks not appearing in Plane

**Cause**: API returned error but script didn't catch it

**Solution**: Check the script output for error messages, verify API key is valid

### "File not found" error

**Cause**: Incorrect file path

**Solution**: Use absolute paths starting with `/Users/joachimtrungtuan/My Documents/Vân Tay Media/Products/Hairline/`

### Rate limiting

**Cause**: Too many API calls in short time (limit: 60/min)

**Solution**: The Python script processes sequentially; if hitting limits, add `time.sleep(1)` between requests

---

## References

- **System Variables**: `local-docs/plane-config/samasu-system-variables.md` - All indexed system IDs
- **API Docs**: https://developers.plane.so/api-reference/introduction
- **Task Files**: `local-docs/task-creation/YYYY-MM-DD/implementation-tasks-*.md`

---

## Changelog

| Date | Change |
|------|--------|
| 2026-02-04 | Added proven Python script method for reliable task creation |
| 2026-02-04 | Documented HTML format requirements for `description_html` field |
| 2026-02-04 | Added troubleshooting section for common issues |
| 2026-01-26 | Initial version with bash-based approach |
