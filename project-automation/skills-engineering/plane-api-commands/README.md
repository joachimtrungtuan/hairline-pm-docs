# Plane API Commands - README

## Quick Reference

This skill provides Python scripts for creating and updating Plane.so issues from markdown task files.

## Scripts

### 1. create-plane-issues.py

**Purpose:** Create NEW Plane issues from markdown task files

**Usage:**

```bash
cd "local-docs/project-automation/task-creation/plane-api"
python3 "../../skills-engineering/plane-api-commands/scripts/create-plane-issues.py" \
  --file "/path/to/tasks.md" \
  [--skip N]
```

**Features:**

- ✅ Automatic HTML cleaning (removes excessive whitespace)
- ✅ Validates all required configuration
- ✅ Skip parameter for partial file processing
- ✅ Clear success/failure reporting with issue IDs

### 2. update-plane-issues.py

**Purpose:** Update EXISTING Plane issues with cleaned descriptions

**Usage:**

```bash
cd "local-docs/project-automation/task-creation/plane-api"
python3 "../../skills-engineering/plane-api-commands/scripts/update-plane-issues.py" \
  --file "/path/to/tasks.md" \
  --start-issue "HAIRL-XXX" \
  [--skip N]
```

**Features:**

- ✅ Updates only `description_html` (preserves all other fields)
- ✅ Automatic HTML cleaning
- ✅ Maps task order to issue sequence automatically
- ✅ Skip parameter for partial file processing

## Prerequisites

1. **Environment file:** `local-docs/project-automation/task-creation/plane-api/.env`
   - Must contain `PLANE_API_KEY`
   - Must contain project/assignee/state/issue type IDs
   - Never commit this file (it's in `.gitignore`)

2. **System variables:** `local-docs/project-automation/task-creation/plane-api/samasu-system-variables.md`
   - Reference for all Plane IDs
   - Update when IDs change

3. **Tools:**
   - Python 3
   - curl (for API calls)

## Task File Format

Task files must use this exact format:

```markdown
## TASK_NAME_START
[PREFIX] Task Name
## TASK_NAME_END

**Status**: Drafted
**FR**: FR-XXX
**Module**: P-XX

## TASK_DESCRIPTION_START
<h2>Overview</h2>
<p>Description content in HTML format</p>
<h2>Reference</h2>
<ul>
<li><a href="...">Link</a></li>
</ul>
<h2>Current Status</h2>
<ul>
<li>Status point</li>
</ul>
<h2>Expectation (Suggestion)</h2>
<p><strong>Note:</strong> Business requirements note...</p>
<ul>
<li>Expectation point</li>
</ul>
<h2>Acceptance Criteria</h2>
<ol>
<li>Criterion</li>
</ol>
## TASK_DESCRIPTION_END
```

**Allowed prefixes:** `[FE+BE TASK]`, `[FE TASK]`, `[BE TASK]`, `[UX/UI TASK]`, `[BUG]`

## Common Scenarios

### Scenario 1: Create all tasks from a new file

```bash
python3 create-plane-issues.py --file "implementation-tasks-2026-02-13-001.md"
```

**Result:** All tasks in file created as new Plane issues

### Scenario 2: Create only tasks 3-10 from a file

```bash
python3 create-plane-issues.py --file "tasks.md" --skip 2
```

**Result:** Skips first 2 tasks, creates tasks 3 onwards

### Scenario 3: Update existing issues with cleaned HTML

```bash
python3 update-plane-issues.py \
  --file "implementation-tasks-2026-02-13-002.md" \
  --start-issue "HAIRL-877"
```

**Result:** Updates all tasks starting from HAIRL-877 with cleaned descriptions

### Scenario 4: Update HAIRL-877 to HAIRL-892 from file with 18 tasks

```bash
python3 update-plane-issues.py \
  --file "tasks.md" \
  --start-issue "HAIRL-877" \
  --skip 2
```

**Result:** Skips first 2 tasks, updates HAIRL-877 (task 3) through HAIRL-892 (task 18)

## HTML Cleaning

Both scripts automatically clean HTML descriptions:

**Before cleaning:**

```html
<h2>Overview</h2>
<p>  Description with    excessive   spaces  </p>

<ul>
<li>  Item with spaces  </li>
</ul>
```

**After cleaning:**

```html
<h2>Overview</h2><p>Description with excessive spaces</p><ul><li>Item with spaces</li></ul>
```

**What gets cleaned:**

- Excessive spaces between HTML tags
- Multiple spaces within text (normalized to single space)
- Leading/trailing whitespace on each line
- Extra blank lines

**What's preserved:**

- HTML structure and tags
- Single spaces in text content
- Link URLs and attributes

## Error Handling

### "Access to '.env' is blocked by security policy"

**Cause:** Running from AI agent context with security sandbox

**Fix:** Run in external terminal (iTerm, Terminal.app, etc.)

```bash
# Open external terminal, then:
cd "/Users/joachimtrungtuan/My Documents/Vân Tay Media/Products/Hairline/local-docs/project-automation/task-creation/plane-api"
python3 "../../skills-engineering/plane-api-commands/scripts/create-plane-issues.py" --file "tasks.md"
```

### "Missing required config in .env"

**Cause:** `.env` file incomplete

**Fix:** Add missing variables to `.env`:

```bash
PLANE_API_KEY=plane_api_...
WORKSPACE_SLUG=samasu-digital
PROJECT_ID=ff2d96b2-0ab2-438b-b879-fbdaa078dbd6
ASSIGNEE_ID=c5bb905a-57bc-4f08-aee0-32d69f8fec78
STAGE_ID=b189d1d2-0d1d-40f9-9a22-7e4ea5f5976f
ISSUE_TYPE_ID=ee71055e-0962-4d04-bab7-e434c1347d8d
```

Reference `samasu-system-variables.md` for current IDs.

### "Could not find issue HAIRL-XXX"

**Cause:** Issue doesn't exist or wrong identifier

**Fix:**

1. Check issue exists in Plane
2. Verify identifier format (HAIRL-XXX)
3. Ensure you're in the correct project

### "No tasks found"

**Cause:** Task file doesn't match expected format

**Fix:**

1. Verify file has `TASK_NAME_START/END` markers
2. Verify file has `TASK_DESCRIPTION_START/END` markers
3. Check for typos in marker names

## Security Notes

- ✅ Scripts load API key from `.env` (never hardcoded)
- ✅ API key is never printed, logged, or exposed
- ✅ `.env` is in `.gitignore` (not committed to git)
- ✅ Documentation references UUIDs from `samasu-system-variables.md`

**NEVER:**

- Hardcode API keys in scripts
- Commit `.env` to version control
- Print or log API keys
- Embed credentials in documentation

## Maintenance

### When to update scripts

1. **Plane API changes** → Update endpoint URLs or payload structure
2. **New HTML cleaning needs** → Enhance `clean_html()` function
3. **New parameters needed** → Add to argparse configuration
4. **Bug fixes** → Update affected functions

### When to update documentation

1. **Script changes** → Update SKILL.md, commands/.md, and workflows/.md files
2. **New features** → Document in all three locations
3. **Common issues discovered** → Add to troubleshooting sections

### Files to keep in sync

- `skills-engineering/plane-api-commands/SKILL.md` (detailed documentation)
- `commands/plane-api-commands.md` (Cursor command format)
- `workflows/plane-api-commands.md` (Antigravity workflow format)

## Testing

Before deploying script changes:

1. **Test create on small file** (2-3 tasks)
2. **Verify HTML cleaning** (check Plane UI)
3. **Test skip parameter** (skip 1 task, verify rest)
4. **Test update on existing issue** (verify preservation of other fields)
5. **Test error handling** (invalid file, missing config)

## Support

For issues or questions:

1. Check troubleshooting section in this README
2. Check "Common Issues" in skill documentation
3. Review recent changes in `IMPROVEMENTS-2026-02-13.md`

---

**Last Updated:** 2026-02-13  
**Version:** 2.0 (with HTML cleaning and update capability)
