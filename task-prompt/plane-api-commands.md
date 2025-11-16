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
3. Tools: `curl`, `jq` (optional), `grep`
4. `PLANE_API_KEY` in `.env` (format: `plane_api_...`)

## Setup

```bash
# Navigate to plane-api directory (where .env file is located)
cd "local-docs/task-creation/plane-api"

# Verify .env file exists
[ ! -f ".env" ] && { echo "ERROR: .env file not found. Copy from .env.example and add your API key."; exit 1; }

# Load environment variables
export $(grep -v '^#' .env | grep -v '^$' | xargs)
BASE_URL="${BASE_URL:-https://api.plane.so/api/v1}"

# Validate API key
[ -z "$PLANE_API_KEY" ] || [ "$PLANE_API_KEY" = "plane_api_your_api_key_here" ] && { echo "ERROR: PLANE_API_KEY not set in .env file"; exit 1; }

# System variables file for alternative IDs
SYSTEM_VARS_FILE="../../plane-config/samasu-system-variables.md"

# Default values (from samasu-system-variables.md)
DEFAULT_PROJECT_ID="${DEFAULT_PROJECT_ID:-ff2d96b2-0ab2-438b-b879-fbdaa078dbd6}"
DEFAULT_ASSIGNEE_ID="${DEFAULT_ASSIGNEE_ID:-c5bb905a-57bc-4f08-aee0-32d69f8fec78}"
DEFAULT_STAGE_ID="${DEFAULT_STAGE_ID:-b189d1d2-0d1d-40f9-9a22-7e4ea5f5976f}"
DEFAULT_PRIORITY="${DEFAULT_PRIORITY:-medium}"
DEFAULT_ISSUE_TYPE_ID="${DEFAULT_ISSUE_TYPE_ID:-ee71055e-0962-4d04-bab7-e434c1347d8d}"
DEFAULT_WORKSPACE_SLUG="${DEFAULT_WORKSPACE_SLUG:-samasu-digital}"
export DEFAULT_PROJECT_ID DEFAULT_ASSIGNEE_ID DEFAULT_STAGE_ID DEFAULT_PRIORITY DEFAULT_ISSUE_TYPE_ID DEFAULT_WORKSPACE_SLUG
```

**CRITICAL**: If defaults not applicable, **MUST** reference `samasu-system-variables.md` for alternative IDs (team members, issue types, states, labels, priorities)

## Markdown Task Format

**CRITICAL**: Only format used. Tasks **MUST** follow this structure:

```markdown
## TASK_NAME_START
[FE+BE TASK] Task Name
## TASK_NAME_END

**Status**: Drafted

## TASK_DESCRIPTION_START
**Overview**: [2-3 sentences]
**Reference**: [GitHub PRD link with anchor]
**Current Status**: [File paths/endpoints]
**Expectation**: [Requirements]
**Acceptance Criteria**: [Testable criteria]
## TASK_DESCRIPTION_END
```

**Prefixes**: `[FE+BE TASK]`, `[FE TASK]`, `[BE TASK]`, `[BUG]` - **DO NOT** remove from task name.

**Status**: `Drafted`, `Confirmed`, `Added to Plane`

## Parse Markdown & Create Tasks

**MUST** when markdown file provided:

1. **Parse tasks**: Extract from `TASK_NAME_START/END` and `TASK_DESCRIPTION_START/END` markers
2. **Create todo list**: `todo_write(merge=false, todos=[{id: "task-1", content: "[FE TASK] Name", status: "pending"}, ...])`
3. **Create tasks**: For each task:
   - Update todo: `todo_write(merge=true, todos=[{id: "task-1", status: "in_progress"}])`
   - Create in Plane.so using defaults (reference `samasu-system-variables.md` if defaults not applicable)
   - Update todo: `completed` (or `cancelled` if fails)

**Parsing**:

```bash
TASK_NAME=$(awk '/## TASK_NAME_START/,/## TASK_NAME_END/ {if (!/TASK_NAME_(START|END)/) print}' "$FILE" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')
TASK_DESCRIPTION=$(awk '/## TASK_DESCRIPTION_START/,/## TASK_DESCRIPTION_END/ {if (!/TASK_DESCRIPTION_(START|END)/) print}' "$FILE")
```

## API Operations

### List Operations Template

```bash
WORKSPACE_SLUG="${WORKSPACE_SLUG:-$1}"
[ -z "$WORKSPACE_SLUG" ] && { echo "ERROR: WORKSPACE_SLUG required"; exit 1; }

# For project-specific: PROJECT_ID="${PROJECT_ID:-$2}"
# [ -z "$PROJECT_ID" ] && { echo "ERROR: PROJECT_ID required"; exit 1; }

curl -s -X GET "$BASE_URL/workspaces/$WORKSPACE_SLUG/[endpoint]/" \
     -H "X-API-Key: $PLANE_API_KEY" | jq '.'
```

**Endpoints**:

- Users: `members/`
- Projects: `projects/`
- Modules: `projects/$PROJECT_ID/modules/`
- Tags: `projects/$PROJECT_ID/labels/`
- Work Item Types: `projects/$PROJECT_ID/issue-types/`
- Stages: `projects/$PROJECT_ID/states/`

### Create Work Item

**Required**: `WORKSPACE_SLUG`, `TITLE` (from markdown, **MUST** include prefix)

**Defaults** (from `samasu-system-variables.md`): Workspace: `samasu-digital`, Project: `ff2d96b2-0ab2-438b-b879-fbdaa078dbd6`, Assignee: `c5bb905a-57bc-4f08-aee0-32d69f8fec78`, Priority: `medium`, State: `b189d1d2-0d1d-40f9-9a22-7e4ea5f5976f`, Issue Type: `ee71055e-0962-4d04-bab7-e434c1347d8d`

**If defaults not applicable**: Reference `samasu-system-variables.md` for alternative IDs (assignees, issue types, states, labels, priorities)

```bash
WORKSPACE_SLUG="${WORKSPACE_SLUG:-${1:-$DEFAULT_WORKSPACE_SLUG}}"
TITLE="${TITLE:-$2}"
DESCRIPTION="${DESCRIPTION:-$3}"
PROJECT_ID="${PROJECT_ID:-$DEFAULT_PROJECT_ID}"
ASSIGNEE_ID="${ASSIGNEE_ID:-$DEFAULT_ASSIGNEE_ID}"
STATE="${STATE:-$DEFAULT_STAGE_ID}"
PRIORITY="${PRIORITY:-$DEFAULT_PRIORITY}"
ISSUE_TYPE="${ISSUE_TYPE:-$DEFAULT_ISSUE_TYPE_ID}"

[ -z "$WORKSPACE_SLUG" ] || [ -z "$TITLE" ] && { echo "ERROR: WORKSPACE_SLUG and TITLE required"; exit 1; }

# If non-default values needed, reference SYSTEM_VARS_FILE for IDs
# Example: grep -A 1 "Mohamed Taha" "$SYSTEM_VARS_FILE" | grep "ID:" | sed 's/.*ID: `\(.*\)`/\1/'

PAYLOAD=$(jq -n \
    --arg name "$TITLE" \
    --arg desc "${DESCRIPTION:-}" \
    --arg project "$PROJECT_ID" \
    --argjson assignees "[ \"$ASSIGNEE_ID\" ]" \
    --arg state "$STATE" \
    --arg priority "$PRIORITY" \
    --arg issue_type "$ISSUE_TYPE" \
    '{name: $name, project: $project, assignees: $assignees, state: $state, priority: $priority, issue_type: $issue_type} + (if $desc != "" then {description: $desc} else {} end)')

curl -s -X POST "$BASE_URL/workspaces/$WORKSPACE_SLUG/projects/$PROJECT_ID/issues/" \
     -H "X-API-Key: $PLANE_API_KEY" \
     -H "Content-Type: application/json" \
     -d "$PAYLOAD" | jq '.'
```

**Without jq**:

```bash
PAYLOAD="{\"name\":\"$TITLE\",\"project\":\"$PROJECT_ID\",\"assignees\":[\"$ASSIGNEE_ID\"],\"state\":\"$STATE\",\"priority\":\"$PRIORITY\",\"issue_type\":\"$ISSUE_TYPE\"}"
[ -n "$DESCRIPTION" ] && PAYLOAD=$(echo "$PAYLOAD" | sed "s/}$/,\"description\":\"$DESCRIPTION\"}/")
curl -s -X POST "$BASE_URL/workspaces/$WORKSPACE_SLUG/projects/$PROJECT_ID/issues/" \
     -H "X-API-Key: $PLANE_API_KEY" -H "Content-Type: application/json" -d "$PAYLOAD" | jq '.'
```

**Lookup examples** (from `$SYSTEM_VARS_FILE`):

```bash
# Assignee: grep -A 1 "Mohamed Taha" "$SYSTEM_VARS_FILE" | grep "ID:" | sed 's/.*ID: `\(.*\)`/\1/'
# State: grep -A 1 "In Progress" "$SYSTEM_VARS_FILE" | grep -E "^-.*`[a-f0-9-]+`" | sed 's/.*`\([a-f0-9-]*\)`.*/\1/'
# Issue Type: grep -A 1 "Epic" "$SYSTEM_VARS_FILE" | grep "ID:" | sed 's/.*ID: `\(.*\)`/\1/'
```

## Error Handling

- **401**: Invalid/expired API key - regenerate
- **404**: Invalid workspace slug or project ID - verify
- **400**: Validation error - check required fields
- **429**: Rate limit (60/min) - check `X-RateLimit-Remaining`, wait for reset
- **5xx**: Server error - retry later

## Pagination

Check for `next_cursor` in response. Fetch next page: `?cursor=$NEXT_CURSOR`

## References

- **System Variables**: `local-docs/plane-config/samasu-system-variables.md` - All indexed system IDs
- API Docs: <https://developers.plane.so/api-reference/introduction>
