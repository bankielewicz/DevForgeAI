#!/bin/bash
# TaskCompleted Hook: Validate step completion against subagent registry
# STORY-527: Checks if required subagent was invoked before marking step complete
# Blocking: exits 2 if required subagent missing, 0 otherwise
#
# Input: JSON on stdin from TaskCompleted event containing subject field
# Output: None (diagnostics to stderr only)
# Exit codes: 0=pass/no-op, 2=block (missing required subagent)

# Safety: never crash the workflow on unexpected errors
trap 'exit 0' ERR

# Read JSON from stdin
INPUT=$(cat 2>/dev/null) || exit 0

# Check jq availability
if ! command -v jq &>/dev/null; then
    echo "WARN: jq not found, cannot validate step completion" >&2
    exit 0
fi

# Extract project root by walking up directory tree
find_project_root() {
    if [ -n "${CLAUDE_PROJECT_DIR:-}" ]; then
        echo "$CLAUDE_PROJECT_DIR"
        return 0
    fi

    if [ -f "CLAUDE.md" ]; then
        pwd
        return 0
    fi

    local dir="$(pwd)"
    while [ "$dir" != "/" ]; do
        if [ -f "$dir/CLAUDE.md" ]; then
            echo "$dir"
            return 0
        fi
        dir="$(dirname "$dir")"
    done

    return 1
}

# Extract subject field
SUBJECT=$(echo "$INPUT" | jq -r '.subject // ""' 2>/dev/null) || exit 0

# Check if subject matches step pattern
if ! echo "$SUBJECT" | grep -qE '^Step [0-9]'; then
    exit 0
fi

# Extract step_id (e.g., "Step 02.2: description" -> "02.2")
STEP_ID=$(echo "$SUBJECT" | sed -E 's/^Step ([0-9][0-9.]*).*/\1/' | sed 's/\.$//')

if [ -z "$STEP_ID" ]; then
    exit 0
fi

echo "DEBUG: TaskCompleted step_id=$STEP_ID" >&2

# Determine project root
PROJECT_ROOT=$(find_project_root)
if [ -z "$PROJECT_ROOT" ]; then
    echo "WARN: Cannot determine project root" >&2
    exit 0
fi

# Load registry
REGISTRY_FILE="${REGISTRY_PATH:-$CLAUDE_PROJECT_DIR/.claude/hooks/phase-steps-registry.json}"

if [ ! -f "$REGISTRY_FILE" ]; then
    echo "DEBUG: Registry not found at $REGISTRY_FILE" >&2
    exit 0
fi

# Validate registry is valid JSON
if ! jq empty "$REGISTRY_FILE" 2>/dev/null; then
    echo "WARN: Malformed registry at $REGISTRY_FILE" >&2
    exit 0
fi

# Look up step by id
STEP_ENTRY=$(jq --arg id "$STEP_ID" '.steps[] | select(.id == $id)' "$REGISTRY_FILE" 2>/dev/null) || exit 0

if [ -z "$STEP_ENTRY" ]; then
    echo "DEBUG: Unknown step $STEP_ID, skipping" >&2
    exit 0
fi

# Check if conditional
IS_CONDITIONAL=$(echo "$STEP_ENTRY" | jq -r '.conditional // false' 2>/dev/null) || exit 0
if [ "$IS_CONDITIONAL" = "true" ]; then
    echo "DEBUG: Step $STEP_ID is conditional, skipping" >&2
    exit 0
fi

# Get subagent field
SUBAGENT_RAW=$(echo "$STEP_ENTRY" | jq -c '.subagent' 2>/dev/null) || exit 0

# null subagent -> no check needed
if [ "$SUBAGENT_RAW" = "null" ]; then
    echo "DEBUG: Step $STEP_ID has no required subagent" >&2
    exit 0
fi

# Extract phase from step_id (part before first dot)
PHASE=$(echo "$STEP_ID" | sed -E 's/^([^.]+)\..*/\1/')

echo "DEBUG: Phase=$PHASE for step $STEP_ID" >&2

# Load phase-state
if [ -n "${PHASE_STATE_PATH:-}" ]; then
    PHASE_STATE_FILE="$PHASE_STATE_PATH"
else
    WORKFLOWS_DIR="$PROJECT_ROOT/devforgeai/workflows"
    if [ ! -d "$WORKFLOWS_DIR" ]; then
        echo "WARN: No workflows directory found" >&2
        exit 0
    fi
    # Find most recent phase-state.json, excluding QA files
    PHASE_STATE_FILE=$(ls -t "$WORKFLOWS_DIR"/STORY-*-phase-state.json 2>/dev/null | grep -v '\-qa-' | head -1) || exit 0
fi

if [ -z "$PHASE_STATE_FILE" ] || [ ! -f "$PHASE_STATE_FILE" ]; then
    echo "WARN: No phase-state file found" >&2
    exit 0
fi

# Get invoked subagents for this phase
INVOKED_JSON=$(jq --arg phase "$PHASE" '.subagents_invoked[$phase] // []' "$PHASE_STATE_FILE" 2>/dev/null) || exit 0

# Determine if subagent is string or array
SUBAGENT_TYPE=$(echo "$SUBAGENT_RAW" | jq -r 'type' 2>/dev/null) || exit 0

if [ "$SUBAGENT_TYPE" = "string" ]; then
    # Single subagent check
    REQUIRED="$( echo "$SUBAGENT_RAW" | jq -r '.' 2>/dev/null )"
    FOUND=$(echo "$INVOKED_JSON" | jq --arg req "$REQUIRED" 'map(select(. == $req)) | length' 2>/dev/null) || exit 0

    if [ "$FOUND" -gt 0 ] 2>/dev/null; then
        echo "DEBUG: Required subagent '$REQUIRED' found for step $STEP_ID" >&2
        exit 0
    else
        echo "BLOCK: Step $STEP_ID requires subagent '$REQUIRED' but it was not invoked. Invoked: $INVOKED_JSON" >&2
        exit 2
    fi

elif [ "$SUBAGENT_TYPE" = "array" ]; then
    # OR-logic: any match passes
    MATCH=$(echo "$SUBAGENT_RAW" | jq --argjson invoked "$INVOKED_JSON" '[.[] as $req | select($invoked | index($req))] | length' 2>/dev/null) || exit 0

    if [ "$MATCH" -gt 0 ] 2>/dev/null; then
        echo "DEBUG: At least one required subagent found for step $STEP_ID" >&2
        exit 0
    else
        echo "BLOCK: Step $STEP_ID requires one of $SUBAGENT_RAW but none were invoked. Invoked: $INVOKED_JSON" >&2
        exit 2
    fi

else
    echo "WARN: Unexpected subagent type '$SUBAGENT_TYPE' for step $STEP_ID" >&2
    exit 0
fi
