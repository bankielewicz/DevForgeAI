#!/bin/bash
################################################################################
# Phase Completion Gate - Stop Event Hook
# STORY-528: Prevent Claude from stopping with incomplete dev workflow phases
#
# Purpose: Block Claude Code "Stop" if any active /dev workflow has incomplete
#          phases. Uses a counter to prevent infinite re-trigger loops.
#
# Exit Codes:
#   0 - Allow stop (all complete, no workflows, counter exceeded, or error)
#   2 - Block stop (incomplete phases found)
#
# Input: JSON on stdin from Stop event
#   - stop_hook_active (boolean): true if re-triggered after previous block
#
# Created: 2026-03-03 (STORY-528)
################################################################################

# Timestamp for log messages
log() {
    local level="$1"
    shift
    echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] [STOP-HOOK] $level - $*" >&2
}

# Safety: never crash the workflow on unexpected errors
trap 'log "ERROR" "Unexpected error on line $LINENO"; exit 0' ERR

# Read JSON from stdin
INPUT=$(cat 2>/dev/null) || exit 0

# Check jq availability
if ! command -v jq &>/dev/null; then
    echo "WARN: jq not found, cannot validate phase completion" >&2
    exit 0
fi

# Extract project root
find_project_root() {
    if [ -n "${CLAUDE_PROJECT_DIR:-}" ]; then
        echo "$CLAUDE_PROJECT_DIR"
        return 0
    fi
    local dir
    dir="$(pwd)"
    while [ "$dir" != "/" ]; do
        if [ -f "$dir/CLAUDE.md" ]; then
            echo "$dir"
            return 0
        fi
        dir="$(dirname "$dir")"
    done
    return 1
}

PROJECT_ROOT=$(find_project_root) || {
    log "ALLOW" "Cannot determine project root"
    exit 0
}

# AC#3 primary loop guard: check stop_hook_active from stdin JSON
STOP_HOOK_ACTIVE=$(echo "$INPUT" | jq -r '.stop_hook_active // false' 2>/dev/null)
if [ "$STOP_HOOK_ACTIVE" = "true" ]; then
    log "ALLOW" "stop_hook_active=true, allowing stop to prevent loop"
    exit 0
fi

WORKFLOWS_DIR="$PROJECT_ROOT/devforgeai/workflows"

# AC#4: No workflows directory or no phase-state files -> allow
if [ ! -d "$WORKFLOWS_DIR" ]; then
    log "ALLOW" "No workflows directory found"
    exit 0
fi

# AC#4: Discover phase-state files, EXCLUDE *-qa-* pattern
mapfile -t PHASE_FILES < <(find "$WORKFLOWS_DIR" -maxdepth 1 -name 'STORY-*-phase-state.json' ! -name '*-qa-*' 2>/dev/null | sort)

if [ ${#PHASE_FILES[@]} -eq 0 ]; then
    log "ALLOW" "No active dev workflows found"
    exit 0
fi

# Check each workflow for incomplete phases
INCOMPLETE_FOUND=false
INCOMPLETE_REPORT=""

for phase_file in "${PHASE_FILES[@]}"; do
    # Graceful degradation: skip malformed JSON
    if ! jq -e '.phases' "$phase_file" >/dev/null 2>&1; then
        log "WARN" "Malformed JSON in $(basename "$phase_file"), skipping"
        continue
    fi

    STORY_ID=$(jq -r '.story_id // "UNKNOWN"' "$phase_file" 2>/dev/null)

    # Extract incomplete phases
    INCOMPLETE_PHASES=$(jq -r '
        .phases | to_entries[]
        | select(.value.completed == false)
        | "\(.key)|\(.value.name // "Unknown")|\(.value.status // "unknown")"
    ' "$phase_file" 2>/dev/null)

    if [ -n "$INCOMPLETE_PHASES" ]; then
        INCOMPLETE_FOUND=true
        while IFS='|' read -r phase_num phase_name phase_status; do
            INCOMPLETE_REPORT+="  - ${STORY_ID}: Phase ${phase_num} (${phase_name}) - Status: ${phase_status}"$'\n'
        done <<< "$INCOMPLETE_PHASES"
    fi
done

# All workflows complete or all malformed -> allow
if [ "$INCOMPLETE_FOUND" = "false" ]; then
    log "ALLOW" "All active dev workflows have completed phases"
    exit 0
fi

# AC#3: Counter file check (max 3 retriggers)
COUNTER_DIR="$PROJECT_ROOT/tmp/STORY-528"
COUNTER_FILE="$COUNTER_DIR/stop-hook-counter"
MAX_RETRIGGERS=3

# Read and validate counter from file
read_counter() {
    local count=0
    if [ -f "$COUNTER_FILE" ]; then
        count=$(cat "$COUNTER_FILE" 2>/dev/null)
        if ! [[ "$count" =~ ^[0-9]+$ ]]; then
            log "WARN" "Counter file corrupted, resetting to 0"
            count=0
        fi
    fi
    echo "$count"
}

# Increment counter and persist to file
increment_counter() {
    local current="$1"
    local next=$((current + 1))
    mkdir -p "$COUNTER_DIR"
    echo "$next" > "$COUNTER_FILE"
    chmod 0600 "$COUNTER_FILE" 2>/dev/null
    echo "$next"
}

CURRENT_COUNT=$(read_counter)

if [ "$CURRENT_COUNT" -ge "$MAX_RETRIGGERS" ]; then
    log "ALLOW" "Max stop-hook retriggers exceeded (count=$CURRENT_COUNT)"
    exit 0
fi

# Block: increment counter and report incomplete phases
NEW_COUNT=$(increment_counter "$CURRENT_COUNT")

# AC#6: Report incomplete phases to stderr
log "BLOCK" "Incomplete dev workflow phases detected"
echo "Incomplete phases:" >&2
echo "$INCOMPLETE_REPORT" >&2
echo "Stop-hook retrigger count: $NEW_COUNT/$MAX_RETRIGGERS" >&2

exit 2
