#!/bin/bash
# .claude/hooks/post-edit-write-check.sh
# PostToolUse hook for Edit|Write — warns when targeting operational files during dev work
# Follows pattern from pre-tool-use.sh

PROJECT_ROOT="${CLAUDE_PROJECT_DIR:-/mnt/c/Projects/DevForgeAI2}"
LOG_FILE="$PROJECT_ROOT/devforgeai/logs/post-edit-write.log"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

mkdir -p "$PROJECT_ROOT/devforgeai/logs" 2>/dev/null

log() {
  echo "[$TIMESTAMP] $1" >> "$LOG_FILE"
}

# Read hook input from stdin
HOOK_INPUT=$(cat)

# Extract file path from tool input
FILE_PATH=$(echo "$HOOK_INPUT" | jq -r '.tool_input.file_path // empty' 2>/dev/null)

if [ -z "$FILE_PATH" ]; then
  exit 0
fi

log "Edit/Write target: $FILE_PATH"

# Operational directories that should NOT be modified during /dev workflows
# These are the runtime/operational copies — source lives in src/
OPERATIONAL_PATTERNS=(
  ".claude/skills/"
  ".claude/agents/"
  ".claude/commands/"
  ".claude/rules/"
)

# Exceptions: files that legitimately live in operational dirs (not mirrored in src/)
EXCEPTION_PATTERNS=(
  ".claude/settings"
  ".claude/hooks/"
  ".claude/plans/"
  ".claude/memory/"
  ".claude/teams/"
  ".claude/tasks/"
  "CLAUDE.md"
)

# Check if file matches an exception first
for exception in "${EXCEPTION_PATTERNS[@]}"; do
  if [[ "$FILE_PATH" == *"$exception"* ]]; then
    log "OK: Exception pattern matched — $exception"
    exit 0
  fi
done

# Check if file is in an operational directory
for pattern in "${OPERATIONAL_PATTERNS[@]}"; do
  if [[ "$FILE_PATH" == *"$pattern"* ]] && [[ "$FILE_PATH" != *"src/"* ]]; then
    log "WARNING: Operational file edited: $FILE_PATH"
    log "Expected: src/ tree equivalent"
    echo "WARNING: You edited an operational file ($FILE_PATH). This project uses a dual-path architecture — development work should target the src/ tree equivalent (e.g., src/claude/...). Verify this edit is intentional and not a src/ file that should be modified instead." >&2
    exit 2
  fi
done

log "OK: $FILE_PATH"
exit 0
