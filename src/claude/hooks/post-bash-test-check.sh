#!/bin/bash
# .claude/hooks/post-bash-test-check.sh
# PostToolUse hook for Bash — reminds to run tests against src/ tree
# Follows pattern from pre-tool-use.sh

PROJECT_ROOT="${CLAUDE_PROJECT_DIR:-/mnt/c/Projects/DevForgeAI2}"
LOG_FILE="$PROJECT_ROOT/devforgeai/logs/post-bash-test.log"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

mkdir -p "$PROJECT_ROOT/devforgeai/logs" 2>/dev/null

log() {
  echo "[$TIMESTAMP] $1" >> "$LOG_FILE"
}

# Read hook input from stdin
HOOK_INPUT=$(cat)

# Extract command from tool input
COMMAND=$(echo "$HOOK_INPUT" | jq -r '.tool_input.command // empty' 2>/dev/null)

if [ -z "$COMMAND" ]; then
  exit 0
fi

# Only check test-related commands
if ! echo "$COMMAND" | grep -qE '(pytest|jest|npm test|npm run test|bash.*test|\.sh)'; then
  exit 0
fi

log "Test command detected: ${COMMAND:0:200}"

# Check if test command references operational dirs instead of src/ or tests/
# Flag: running tests against .claude/ directly (should use src/ tree)
OPERATIONAL_TEST_PATTERNS=(
  "pytest .claude/"
  "pytest ./.claude/"
  "bash .claude/"
  "bash ./.claude/"
  ".claude/scripts/devforgeai_cli/tests/"
)

for pattern in "${OPERATIONAL_TEST_PATTERNS[@]}"; do
  if [[ "$COMMAND" == *"$pattern"* ]]; then
    log "WARNING: Test running against operational dir: $COMMAND"
    echo "Reminder: Tests should run against the src/ tree, not operational folders. WSL has historically generated corrupt or missing file errors when testing against operational directories. Use src/ equivalents instead." >&2
    exit 2
  fi
done

log "OK: Test command targets correct tree"
exit 0
