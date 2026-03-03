#!/bin/bash
# SessionStart Hook: Progressive Context Injection
# STORY-529 - Injects workflow state after resume/compact events
# Always exits 0 (non-blocking)

# Do NOT use set -e — hook must always exit 0
set -o pipefail 2>/dev/null || true

PROJECT_DIR="${CLAUDE_PROJECT_DIR:-.}"
WORKFLOWS_DIR="$PROJECT_DIR/devforgeai/workflows"

# --- Helper: emit warning to stderr ---
warn() {
    echo "[inject-phase-context] WARNING: $*" >&2
}

# --- Check workflows directory exists ---
if [ ! -d "$WORKFLOWS_DIR" ]; then
    warn "No workflows directory found at $WORKFLOWS_DIR"
    exit 0
fi

# --- Find phase-state files, excluding QA files ---
PHASE_FILES=()
while IFS= read -r -d '' file; do
    PHASE_FILES+=("$file")
done < <(find "$WORKFLOWS_DIR" -maxdepth 1 -name '*-phase-state.json' -not -name '*-qa-*' -print0 2>/dev/null)

if [ ${#PHASE_FILES[@]} -eq 0 ]; then
    warn "No active phase-state files found (QA files excluded)"
    exit 0
fi

# --- Select most recent by "created" timestamp ---
MOST_RECENT_FILE=""
MOST_RECENT_TS=""

for file in "${PHASE_FILES[@]}"; do
    # Skip empty files
    if [ ! -s "$file" ]; then
        warn "Skipping empty file: $file"
        continue
    fi

    # Parse created timestamp, skip malformed JSON
    TS=$(jq -r '.created // empty' "$file" 2>/dev/null)
    if [ -z "$TS" ]; then
        warn "Skipping file with missing/invalid created field: $file"
        continue
    fi

    if [ -z "$MOST_RECENT_TS" ] || [[ "$TS" > "$MOST_RECENT_TS" ]]; then
        MOST_RECENT_TS="$TS"
        MOST_RECENT_FILE="$file"
    fi
done

if [ -z "$MOST_RECENT_FILE" ]; then
    warn "No valid phase-state files found after parsing"
    exit 0
fi

# --- Extract workflow data ---
STORY_ID=$(jq -r '.story_id // "unknown"' "$MOST_RECENT_FILE" 2>/dev/null)
CURRENT_PHASE=$(jq -r '.current_phase // "unknown"' "$MOST_RECENT_FILE" 2>/dev/null)

# Get phase name for current phase
PHASE_NAME=$(jq -r ".phases[\"$CURRENT_PHASE\"].name // \"unknown\"" "$MOST_RECENT_FILE" 2>/dev/null)

# Count completed and total phases
STEPS_COMPLETED=$(jq '[.phases // {} | to_entries[] | select(.value.completed == true)] | length' "$MOST_RECENT_FILE" 2>/dev/null || echo "0")
STEPS_TOTAL=$(jq '[.phases // {} | to_entries[]] | length' "$MOST_RECENT_FILE" 2>/dev/null || echo "0")
STEPS_REMAINING=$((STEPS_TOTAL - STEPS_COMPLETED))

# Get subagents invoked
SUBAGENTS_INVOKED=$(jq -r '(.subagents_invoked // []) | join(", ")' "$MOST_RECENT_FILE" 2>/dev/null || echo "none")
SUBAGENTS_COUNT=$(jq '(.subagents_invoked // []) | length' "$MOST_RECENT_FILE" 2>/dev/null || echo "0")

# --- Build additionalContext string ---
CONTEXT="Active Workflow: ${STORY_ID}
Current Phase: ${CURRENT_PHASE} - ${PHASE_NAME}
Steps completed: ${STEPS_COMPLETED} of ${STEPS_TOTAL}
Steps remaining: ${STEPS_REMAINING}
Subagents invoked: ${SUBAGENTS_INVOKED}
Subagents required: See phase ${CURRENT_PHASE} specification for remaining required subagents"

# --- Output JSON to stdout ---
jq -n \
    --arg ctx "$CONTEXT" \
    '{
        "hookSpecificOutput": {
            "hookEventName": "SessionStart",
            "additionalContext": $ctx
        }
    }'

exit 0
