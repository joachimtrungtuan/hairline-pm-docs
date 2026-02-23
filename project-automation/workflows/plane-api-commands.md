---
description: Run Plane.so API operations — list workspace resources or bulk-create issues from implementation task markdown files.
---

# Plane API Commands

Run Plane.so API workflows for listing resources and bulk-creating work items from local task markdown files. All credentials loaded from environment files — never hardcode or expose API keys.

## Supported Operations

Ask user to choose if not specified: `list-users`, `list-projects`, `list-modules`, `list-tags`, `list-work-item-types`, `list-stages`, `create-work-item`

## Prerequisites

- `.env` at `local-docs/project-automation/task-creation/plane-api/.env` with `PLANE_API_KEY`
- System variables at `local-docs/project-automation/task-creation/plane-api/samasu-system-variables.md`
- Tools: `python3`, `curl` (`jq` optional)

## Credential Rules (CRITICAL)

- ALWAYS load `PLANE_API_KEY` from `.env` file
- NEVER hardcode, print, echo, log, or embed the API key in scripts, output, or commits
- If `.env` missing or key empty, ask user to create/populate it
- If permission denied, ask user to grant file access — do not request key in plain text

## Default Configuration

Load IDs from `samasu-system-variables.md`. Defaults: `WORKSPACE_SLUG=samasu-digital`, `BASE_URL=https://api.plane.so/api/v1`. For project/assignee/stage/priority/issue type IDs: always reference config file, never hardcode UUIDs.

## Task File Contract

Required block format for creating issues:

```
## TASK_NAME_START
[PREFIX] Task Name
## TASK_NAME_END

**Status**: Drafted

## TASK_DESCRIPTION_START
<h2>Overview</h2>
<p>...</p>
## TASK_DESCRIPTION_END
```

Prefixes: `[FE+BE TASK]`, `[FE TASK]`, `[BE TASK]`, `[BUG]`, `[UX/UI TASK]`
Statuses: `Drafted`, `Confirmed`, `Added to Plane`
Description must be valid HTML for Plane.so `description_html` field.

## Steps

1. Ask user which operation to run (list or create).

// turbo
2. Load credentials using Python (not bash source):
```python
env_path = "local-docs/project-automation/task-creation/plane-api/.env"
env_vars = {}
with open(env_path) as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith('#') and '=' in line:
            key, value = line.split('=', 1)
            env_vars[key.strip()] = value.strip().strip('"').strip("'")
api_key = env_vars.get("PLANE_API_KEY", "")
```

3. For **list operations**: run curl against `https://api.plane.so/api/v1/workspaces/samasu-digital/...` with API key header. Display formatted results.

4. For **create-work-item** or **update-work-item**: 

Ask user:
- Which operation (create new or update existing)?
- Implementation task file path
- If updating: starting issue identifier (e.g., HAIRL-877)
- If needed: number of tasks to skip from beginning of file

The scripts at `local-docs/project-automation/skills-engineering/plane-api-commands/scripts/` are maintained and include HTML cleaning. Use them directly — do not recreate unless explicitly needed.

**Key improvements in current scripts:**
- HTML cleaning function removes excessive whitespace
- Support for `--skip N` parameter to handle partial file processing
- Better error handling and reporting
- Update script can modify existing issues without recreating them

// turbo
5. Execute the appropriate script:

**For CREATE (new issues):**
```bash
cd "local-docs/project-automation/task-creation/plane-api" && \
python3 "../../skills-engineering/plane-api-commands/scripts/create-plane-issues.py" \
--file "/absolute/path/to/implementation-tasks-YYYY-MM-DD-XXX.md" \
[--skip N]
```

**For UPDATE (existing issues with cleaned HTML):**
```bash
cd "local-docs/project-automation/task-creation/plane-api" && \
python3 "../../skills-engineering/plane-api-commands/scripts/update-plane-issues.py" \
--file "/absolute/path/to/implementation-tasks-YYYY-MM-DD-XXX.md" \
--start-issue "HAIRL-XXX" \
[--skip N]
```

**Examples:**

Create all tasks:
```bash
python3 create-plane-issues.py --file "implementation-tasks-2026-02-13-001.md"
```

Update HAIRL-877 to HAIRL-892, skipping first 2 tasks in file:
```bash
python3 update-plane-issues.py \
--file "implementation-tasks-2026-02-13-002.md" \
--start-issue "HAIRL-877" \
--skip 2
```

6. Report results: total tasks found/created/updated, task-to-issue-ID mapping, any errors with fixes.

## Key Improvements (What Changed)

Previous versions had issues:
1. ❌ No HTML cleaning → excessive whitespace in Plane descriptions
2. ❌ No update capability → had to recreate issues to fix formatting
3. ❌ No skip parameter → couldn't handle partial file processing
4. ❌ Security policy blocks when accessing `.env` from skill execution

Current version fixes:
1. ✅ HTML cleaning function removes excessive whitespace automatically
2. ✅ Update script can modify existing issues (only `description_html` field)
3. ✅ Skip parameter for both create and update scripts
4. ✅ Clear instructions to run in external terminal if `.env` access is blocked
5. ✅ Better error messages and validation

## Why Python (not bash)

`json.dumps()` correctly escapes quotes, newlines, and HTML in multiline descriptions. Lower failure rate than bash string quoting. Clearer error handling.

## API Reference

| Operation | Method | Endpoint |
|-----------|--------|----------|
| List Users | GET | `/workspaces/{slug}/members/` |
| List Projects | GET | `/workspaces/{slug}/projects/` |
| List Modules | GET | `/workspaces/{slug}/projects/{id}/modules/` |
| List Tags | GET | `/workspaces/{slug}/projects/{id}/labels/` |
| List Issue Types | GET | `/workspaces/{slug}/projects/{id}/issue-types/` |
| List States | GET | `/workspaces/{slug}/projects/{id}/states/` |
| Create Issue | POST | `/workspaces/{slug}/projects/{id}/issues/` |

### Create Issue Payload

```json
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

## Error Reference

| Code | Meaning | Fix |
|------|---------|-----|
| 401 | Invalid/expired key | Regenerate in Plane settings, update `.env` |
| 400 | Validation error | Check fields and HTML format |
| 404 | Invalid IDs | Verify in `samasu-system-variables.md` |
| 429 | Rate limit (60/min) | Add delay |
| 5xx | Server error | Retry with backoff |

## Common Issues and Solutions

### Issue: "ERROR: Access to '\.env' is blocked by security policy"

**Symptom:** Script execution fails when trying to read `.env` file from within AI agent context.

**Root Cause:** Security sandbox blocks access to credential files.

**Solution:** Run the command in an external terminal (iTerm, Terminal.app) where file access is not restricted:
1. Open a terminal application
2. Navigate to: `cd "local-docs/project-automation/task-creation/plane-api"`
3. Run the Python script directly with full paths
4. The `.env` file in that directory will be accessible

### Issue: Excessive whitespace in Plane issue descriptions

**Symptom:** Task descriptions in Plane have multiple blank lines, excessive spaces between HTML tags.

**Root Cause:** Original markdown had formatting whitespace that wasn't cleaned before sending to Plane API.

**Solution:** 
- For NEW tasks: Use `create-plane-issues.py` (includes HTML cleaning automatically)
- For EXISTING tasks: Use `update-plane-issues.py` to clean descriptions in place

### Issue: Tasks created in wrong order or with wrong issue numbers

**Symptom:** Script processes tasks that shouldn't be included, or maps to wrong Plane issue IDs.

**Root Cause:** Task file may contain tasks already processed or unrelated tasks at the beginning.

**Solution:** Use `--skip N` parameter:
1. Count how many tasks at the start of the file should be skipped
2. Add `--skip N` to command line
3. For update operations, ensure `--start-issue` matches the first task after skipping

**Example:** File has 18 tasks, first 2 already processed, want to handle tasks 3-18 starting at HAIRL-877:
```bash
python3 update-plane-issues.py \
--file "tasks.md" \
--start-issue "HAIRL-877" \
--skip 2
```

### Issue: Script fails with "Missing required config in .env"

**Symptom:** `PROJECT_ID`, `ASSIGNEE_ID`, `STAGE_ID`, or `ISSUE_TYPE_ID` not found.

**Root Cause:** `.env` file incomplete.

**Solution:**
1. Open `local-docs/project-automation/task-creation/plane-api/.env`
2. Compare with `samasu-system-variables.md`
3. Add missing variables with correct UUIDs
4. Never commit `.env` to git (it's in `.gitignore`)

## References

- System IDs: `local-docs/project-automation/task-creation/plane-api/samasu-system-variables.md`
- Task artifacts: `local-docs/project-automation/task-creation/YYYY-MM-DD/implementation-tasks-*.md`
- Plane API docs: https://developers.plane.so/api-reference/introduction
- Scripts location: `local-docs/project-automation/skills-engineering/plane-api-commands/scripts/`

## Deployment

Copy this file to `.agent/workflows/plane-api-commands.md` for Antigravity to detect it.
