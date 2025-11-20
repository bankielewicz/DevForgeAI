#!/bin/bash
# .claude/hooks/pre-tool-use.sh - DevForgeAI validation hook

# Logging setup
PROJECT_ROOT="${CLAUDE_PROJECT_DIR:-/mnt/c/Projects/DevForgeAI2}"
LOG_FILE="$PROJECT_ROOT/.devforgeai/logs/pre-tool-use.log"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

# Create log directory if needed
mkdir -p "$PROJECT_ROOT/.devforgeai/logs" 2>/dev/null

# Log function
log() {
  echo "[$TIMESTAMP] $1" >> "$LOG_FILE"
}

log "========== HOOK INVOKED =========="

# Read tool input
TOOL_INPUT=$(cat)
log "Raw input length: ${#TOOL_INPUT} chars"
log "Input preview: ${TOOL_INPUT:0:200}..."

# Extract command
COMMAND=$(echo "$TOOL_INPUT" | jq -r '.tool_input.command // empty' 2>/dev/null)
EXTRACT_STATUS=$?

log "jq extraction exit code: $EXTRACT_STATUS"
log "Extracted command: '$COMMAND'"

if [ -z "$COMMAND" ]; then
  log "WARNING: Command is empty after extraction"
  log "Full input: $TOOL_INPUT"
fi

# Auto-approve safe DevForgeAI patterns
SAFE_PATTERNS=(
  "npm run test"
  "npm run build"
  "npm run lint"  
  "dotnet test"
  "dotnet build"
  "git status"
  "git diff"
  "git add"
  "git commit"
  "git log"
  "wc -"
  "bash tests/"
  "bash .claude/scripts/"
  "bash .devforgeai/"
  "echo "
  "cat tests/"
  "cat .devforgeai/"
  "cat >"
  "cat <<"
  "cat << 'EOF'"
  "cp"
  "grep -E"
  "head -"
  "tail -"
  "mkdir -p"
  "chmod +x"
  "dos2unix"
  "sed -i"
  "python3 -m json.tool"
  "python3 <<"
  "python -m pytest"
  "python3 -m pytest"
  "python3 << 'EOF'"
  "python3 << 'EOF'
   import re"
  "pytest"
  "wc -l"
  "ls -la"
  "ls -lh"
  "ls -1"
  "cat src/"
  "cat installer/"
  "find installer"
  "find /mnt/c/Projects/DevForgeAI2/installer"
  "find /mnt/c/Projects/DevForgeAI2/src"
  "find /mnt/c/Projects/DevForgeAI2/tests"
  "grep -r"
  "python3 -m py_compile"
  "sort -"
)

log "Checking against ${#SAFE_PATTERNS[@]} safe patterns..."

# Simple approach: Check if command STARTS WITH safe pattern
# Pattern matching handles pipes/redirects automatically
for pattern in "${SAFE_PATTERNS[@]}"; do
  if [[ "$COMMAND" == "$pattern"* ]]; then
    log "✓ MATCHED safe pattern: '$pattern'"
    log "Decision: AUTO-APPROVE (exit 0)"
    log "=========================================="
    exit 0  # Auto-approve
  fi
done

log "No safe pattern matched"

# Block anti-patterns
BLOCKED_PATTERNS=(
  "rm -rf"
  "sudo"
  "git push"
  "npm publish"
  "curl"
  "wget"
)

log "Checking against ${#BLOCKED_PATTERNS[@]} blocked patterns..."

for pattern in "${BLOCKED_PATTERNS[@]}"; do
  if [[ "$COMMAND" =~ ${pattern} ]]; then
    log "✗ MATCHED blocked pattern: '$pattern'"
    log "Decision: BLOCK (exit 2)"
    log "Sending error to Claude: Dangerous operation: $COMMAND"
    log "=========================================="
    echo '{"decision": "block", "reason": "Dangerous operation: '"$COMMAND"'"}' >&2
    exit 2
  fi
done

log "No blocked pattern matched"

# For all others, ask user for approval
log "Decision: ASK USER (exit 1)"
log "Command requires manual approval: $COMMAND"
log "=========================================="
exit 1