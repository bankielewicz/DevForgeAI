#!/bin/bash
# SubagentStop Hook: Auto-track subagent invocations
# STORY-526: Records DevForgeAI subagent invocations to phase-state.json
# Non-blocking: Always exits 0
#
# Input: JSON on stdin from SubagentStop event containing agent_type field
# Output: None (logs to stderr only)
# Side effect: Calls devforgeai-validate phase-record for DevForgeAI subagents

# Ensure we never block the workflow
trap 'exit 0' ERR

# Read JSON from stdin
INPUT=$(cat 2>/dev/null) || exit 0

# Parse agent_type with jq
if ! command -v jq &>/dev/null; then
    echo "WARN: jq not found, cannot parse SubagentStop event" >&2
    exit 0
fi

AGENT_TYPE=$(echo "$INPUT" | jq -r '.agent_type // ""' 2>/dev/null) || exit 0

# No agent_type found
if [ -z "$AGENT_TYPE" ]; then
    echo "WARN: No agent_type in SubagentStop event" >&2
    exit 0
fi

echo "DEBUG: SubagentStop agent_type=$AGENT_TYPE" >&2

# Filter built-in agents (not DevForgeAI subagents)
BUILTIN_AGENTS="Explore Plan Bash general-purpose"
for builtin in $BUILTIN_AGENTS; do
    if [ "$AGENT_TYPE" = "$builtin" ]; then
        echo "DEBUG: Filtered built-in agent: $AGENT_TYPE" >&2
        exit 0
    fi
done

# Validate agent_type against safe regex (security - NFR-002)
if ! echo "$AGENT_TYPE" | grep -qE '^[a-zA-Z0-9_-]+$'; then
    echo "WARN: Invalid agent_type format: $AGENT_TYPE" >&2
    exit 0
fi

# Determine project root (where CLAUDE.md exists)
PROJECT_ROOT=""
if [ -n "${CLAUDE_PROJECT_DIR:-}" ]; then
    PROJECT_ROOT="$CLAUDE_PROJECT_DIR"
elif [ -f "CLAUDE.md" ]; then
    PROJECT_ROOT="$(pwd)"
else
    # Walk up to find project root
    DIR="$(pwd)"
    while [ "$DIR" != "/" ]; do
        if [ -f "$DIR/CLAUDE.md" ]; then
            PROJECT_ROOT="$DIR"
            break
        fi
        DIR="$(dirname "$DIR")"
    done
fi

if [ -z "$PROJECT_ROOT" ]; then
    echo "WARN: Cannot determine project root" >&2
    exit 0
fi

# Find active story from phase-state.json files
WORKFLOWS_DIR="$PROJECT_ROOT/devforgeai/workflows"
if [ ! -d "$WORKFLOWS_DIR" ]; then
    echo "WARN: No workflows directory found" >&2
    exit 0
fi

# Find most recently modified phase-state.json (the active story)
LATEST_STATE=$(ls -t "$WORKFLOWS_DIR"/STORY-*-phase-state.json 2>/dev/null | head -1) || exit 0

if [ -z "$LATEST_STATE" ]; then
    echo "WARN: No phase-state files found" >&2
    exit 0
fi

# Extract story ID from filename (STORY-NNN-phase-state.json -> STORY-NNN)
FILENAME=$(basename "$LATEST_STATE")
# Extract STORY-NNN from filename like "STORY-526-phase-state.json"
STORY_ID=$(echo "$FILENAME" | sed 's/-phase-state\.json$//')

if [ -z "$STORY_ID" ]; then
    echo "WARN: Cannot extract story ID from $FILENAME" >&2
    exit 0
fi

# Extract current phase from phase-state.json
CURRENT_PHASE=$(jq -r '.current_phase // empty' "$LATEST_STATE" 2>/dev/null) || exit 0

if [ -z "$CURRENT_PHASE" ]; then
    echo "WARN: Cannot determine current phase from $LATEST_STATE" >&2
    exit 0
fi

echo "INFO: Recording subagent $AGENT_TYPE for $STORY_ID phase $CURRENT_PHASE" >&2

# Call devforgeai-validate phase-record
if command -v devforgeai-validate &>/dev/null; then
    devforgeai-validate phase-record "$STORY_ID" \
        --phase="$CURRENT_PHASE" \
        --subagent="$AGENT_TYPE" \
        --project-root="$PROJECT_ROOT" 2>&1 >/dev/null || true
else
    echo "WARN: devforgeai-validate not found, cannot record subagent" >&2
fi

exit 0
