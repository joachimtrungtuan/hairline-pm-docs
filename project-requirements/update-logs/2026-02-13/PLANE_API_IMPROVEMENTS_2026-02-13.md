# Plane API Commands - Improvements Summary

**Date:** 2026-02-13  
**Scope:** `plane-api-commands` skill, command, and workflow updates

## Issues Identified

### 1. Missing HTML Cleaning Function ❌

**Problem:** Task descriptions sent to Plane contained excessive whitespace:

- Multiple spaces between HTML tags (e.g., `<h2> </h2>` instead of `<h2></h2>`)
- Multiple blank lines within content
- Unnecessary whitespace at line beginnings/endings

**Impact:** Plane issue descriptions looked unprofessional with excessive spacing.

**Root Cause:** The `parse_tasks()` function in `create-plane-issues.py` didn't clean HTML before returning descriptions.

### 2. No Update Capability ❌

**Problem:** Could only CREATE new issues, not UPDATE existing ones.

**Impact:**

- To fix HTML formatting issues, had to:
  1. Delete old issues manually
  2. Recreate them with fixed script
- Created duplicate issues
- Lost issue history and comments

**Root Cause:** Only `create-plane-issues.py` existed; no update script.

### 3. No Skip Parameter ❌

**Problem:** Scripts always processed entire file from beginning to end.

**Impact:**

- Couldn't handle files where only a subset of tasks needed processing
- Had to manually edit task files to remove unwanted tasks
- Risk of processing wrong tasks

**Root Cause:** Scripts didn't support `--skip N` parameter.

### 4. Security Policy Blocks `.env` Access ❌

**Problem:** When running from AI agent context, sandbox security blocked reading `.env` file.

**Error Message:** `"ERROR: Access to '\.env' is blocked by security policy"`

**Impact:** Script couldn't load Plane API credentials, workflow failed.

**Root Cause:** AI agent security sandbox restricts file access to credential files.

## Solutions Implemented

### 1. HTML Cleaning Function ✅

**What was added:**

```python
def clean_html(html: str) -> str:
    """Clean HTML by removing excessive whitespace while preserving structure."""
    # Remove excessive spaces between tags
    html = re.sub(r'>\s+<', '><', html)
    # Normalize multiple spaces to single space within text content
    html = re.sub(r'  +', ' ', html)
    # Remove leading/trailing whitespace from each line
    lines = [line.strip() for line in html.split('\n') if line.strip()]
    # Join with no extra newlines
    return ''.join(lines)
```

**Location:** Added to both `create-plane-issues.py` and `update-plane-issues.py`

**Called in:** `parse_tasks()` function before returning task descriptions

**Result:**

- Clean, compact HTML in Plane descriptions
- Professional appearance
- No excessive whitespace

### 2. Update Script Created ✅

**New file:** `local-docs/project-automation/skills-engineering/plane-api-commands/scripts/update-plane-issues.py`

**Features:**

- Updates ONLY the `description_html` field (preserves all other fields)
- Maps issue identifiers (HAIRL-XXX) to internal UUIDs automatically
- Uses PATCH endpoint instead of POST
- Includes HTML cleaning
- Supports `--skip` parameter

**Usage:**

```bash
python3 update-plane-issues.py \
--file "tasks.md" \
--start-issue "HAIRL-877" \
--skip 2
```

**Result:**

- Can clean up existing issues without recreating
- No lost history or comments
- No duplicate issues

### 3. Skip Parameter Added ✅

**Added to:** Both `create-plane-issues.py` and `update-plane-issues.py`

**Usage:**

- `--skip N` where N is number of tasks to skip from beginning of file
- Useful for partial file processing

**Example scenarios:**

1. **File has 18 tasks, first 2 already processed:**

   ```bash
   python3 create-plane-issues.py --file "tasks.md" --skip 2
   ```

   Creates tasks 3-18 only.

2. **Update HAIRL-877 to HAIRL-892 from file with 18 tasks:**

   ```bash
   python3 update-plane-issues.py \
   --file "tasks.md" \
   --start-issue "HAIRL-877" \
   --skip 2
   ```

   Skips first 2 tasks, updates HAIRL-877 (task 3) through HAIRL-892 (task 18).

**Result:**

- Flexible partial file processing
- No need to edit task files
- Precise control over which tasks to process

### 4. Security Policy Workaround ✅

**Solution:** Added clear instructions for running in external terminal.

**Updated documentation with:**

- Troubleshooting section for "Access to '\.env' is blocked"
- Instructions to run in iTerm or Terminal.app
- Explanation that external terminals have unrestricted file access

**Result:**

- Users know how to work around sandbox restrictions
- Scripts work reliably when run from proper context

## Files Updated

### 1. Skills (SKILL.md)

**File:** `local-docs/project-automation/skills-engineering/plane-api-commands/SKILL.md`

**Changes:**

- Added documentation for both create and update scripts
- Added HTML cleaning function documentation
- Added skip parameter usage examples
- Added API reference for UPDATE endpoint
- Added examples for common scenarios

### 2. Commands (.md)

**File:** `local-docs/project-automation/commands/plane-api-commands.md` (CREATED)

**Status:** Was missing, now created

**Contents:**

- Full workflow for both create and update operations
- HTML cleaning function documentation
- Skip parameter usage
- Common issues and solutions section
- Progress tracking requirements

### 3. Workflows (.md)

**File:** `local-docs/project-automation/workflows/plane-api-commands.md`

**Changes:**

- Removed embedded Python script (scripts are maintained separately)
- Added reference to maintained scripts
- Added documentation for update operation
- Added "Key Improvements" section
- Added "Common Issues and Solutions" section
- Added examples for both create and update with skip parameter

### 4. Scripts (Python)

**Files:**

- `local-docs/project-automation/skills-engineering/plane-api-commands/scripts/create-plane-issues.py` (updated)
- `local-docs/project-automation/skills-engineering/plane-api-commands/scripts/update-plane-issues.py` (created)

**Changes:**

Both scripts now include:

- `clean_html()` function
- `--skip N` parameter support
- Better error handling
- Clear success/failure reporting

Update script additionally includes:

- `get_issue_id()` to map identifiers to UUIDs
- `--start-issue` parameter
- PATCH endpoint usage

## Testing Results

### Test 1: Create with HTML Cleaning ✅

**File:** `implementation-tasks-2026-02-13-003.md` (3 UX/UI tasks)

**Command:**

```bash
python3 create-plane-issues.py --file "implementation-tasks-2026-02-13-003.md"
```

**Result:** 3 of 3 tasks created successfully with clean HTML

**Issue IDs:** ebb2f7dd, ed618044, 762c22f4

### Test 2: Update Existing Issues ✅

**File:** `implementation-tasks-2026-02-13-002.md` (18 tasks)

**Command:**

```bash
python3 update-plane-issues.py \
--file "implementation-tasks-2026-02-13-002.md" \
--start-issue "HAIRL-877" \
--skip 2
```

**Result:** 16 of 16 tasks updated successfully (HAIRL-877 through HAIRL-892)

**Outcome:** All descriptions cleaned, no excessive whitespace

## Best Practices Going Forward

### When to Use Each Script

| Scenario | Script to Use | Parameters |
|----------|---------------|------------|
| Creating new issues from scratch | `create-plane-issues.py` | `--file` + optional `--skip` |
| Fixing HTML formatting in existing issues | `update-plane-issues.py` | `--file` + `--start-issue` + optional `--skip` |
| Creating subset of tasks from file | `create-plane-issues.py` | `--file` + `--skip N` |
| Updating subset of existing issues | `update-plane-issues.py` | `--file` + `--start-issue` + `--skip N` |

### File Access Best Practices

1. **Always run from external terminal** when credentials are involved
2. **Never hardcode API keys** in scripts or documentation
3. **Keep `.env` in `.gitignore`** to prevent accidental commits
4. **Reference `samasu-system-variables.md`** for system IDs, don't hardcode UUIDs

### HTML Formatting Best Practices

1. **Always use HTML format** for task descriptions (not plain text)
2. **Let the script clean HTML** - don't manually format for compactness
3. **Include proper sections** (Overview, Reference, Current Status, Expectation, Acceptance Criteria)
4. **Use GitHub links** for references, not local file paths

## Deployment Checklist

To deploy these improvements to other environments:

- [x] Update SKILL.md in skills-engineering folder
- [x] Create/update .md file in commands folder
- [x] Update .md file in workflows folder
- [x] Create update-plane-issues.py script
- [x] Update create-plane-issues.py with HTML cleaning
- [ ] Copy .md to `.cursor/rules/` (for Cursor)
- [ ] Copy .md to `.agent/workflows/` (for Antigravity)
- [ ] Copy skills folder to `.agents/skills/` (for Codex)

## Next Steps

1. ✅ Test both scripts on real task files
2. ✅ Verify HTML cleaning works correctly
3. ✅ Update all documentation
4. ⏳ Deploy to IDE configuration folders (.cursor, .agent, .agents)
5. ⏳ Document in project wiki or README
6. ⏳ Train team on new capabilities

## Summary

**Before:** Could only create issues, no HTML cleaning, no partial file processing, sandbox security issues

**After:** Can create AND update issues, automatic HTML cleaning, flexible skip parameter, clear workarounds for security restrictions

**Impact:** Faster workflow, cleaner Plane issues, no need to manually edit files or recreate issues

---

**Maintained by:** AI Assistant  
**Last Updated:** 2026-02-13  
**Status:** Production Ready ✅
