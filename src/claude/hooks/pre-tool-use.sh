#!/bin/bash
# .claude/hooks/pre-tool-use.sh - DevForgeAI validation hook
# Blocks writes to operational directories and enforces path conventions

# Logging setup
PROJECT_ROOT="${CLAUDE_PROJECT_DIR:-/mnt/c/Projects/DevForgeAI2}"
LOG_FILE="$PROJECT_ROOT/devforgeai/logs/pre-tool-use.log"
UNKNOWN_COMMANDS_LOG="$PROJECT_ROOT/devforgeai/logs/hook-unknown-commands.log"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

# Create log directory if needed
mkdir -p "$PROJECT_ROOT/devforgeai/logs" 2>/dev/null

# Log function
log() {
  echo "[$TIMESTAMP] $1" >> "$LOG_FILE"
}

# Log unknown commands that require manual approval
log_unknown_command() {
  local cmd="$1"
  echo "[$TIMESTAMP] UNKNOWN COMMAND REQUIRING APPROVAL: $cmd" >> "$UNKNOWN_COMMANDS_LOG"
}

log "========== HOOK INVOKED =========="

# Read tool input from stdin
TOOL_INPUT=$(cat)
log "Raw input length: ${#TOOL_INPUT} chars"
log "Input preview: ${TOOL_INPUT:0:200}..."

# Detect tool name from input
TOOL_NAME=$(echo "$TOOL_INPUT" | jq -r '.tool_name // empty' 2>/dev/null)
log "Tool name: '$TOOL_NAME'"

# ============================================================
# SECTION 1: Edit/Write PATH ENFORCEMENT (Insights recommendation)
# Blocks writes to operational .claude/ dirs (except whitelisted),
# /tmp/ usage, and src/tests/ (must use tests/{story-id}/)
# ============================================================
if [[ "$TOOL_NAME" == "Edit" || "$TOOL_NAME" == "Write" ]]; then
  FILE_PATH=$(echo "$TOOL_INPUT" | jq -r '.tool_input.file_path // empty' 2>/dev/null)
  log "Write/Edit target: '$FILE_PATH'"

  # --- Whitelist: .claude/plans/ and .claude/memory/sessions/ are always OK ---
  if [[ "$FILE_PATH" == *"/.claude/plans/"* || "$FILE_PATH" == *"/.claude/memory/sessions/"* ]]; then
    log "✓ Whitelisted operational path: $FILE_PATH"
    # Fall through to Bash command checks (don't exit yet, let normal flow handle)

  # --- BLOCK: .claude/ operational directories (not whitelisted) ---
  elif [[ "$FILE_PATH" == *"/.claude/"* ]]; then
    log "✗ BLOCKED: Write to operational .claude/ directory"
    log "  Target: $FILE_PATH"

    # Suggest the src/ equivalent
    SUGGESTED=$(echo "$FILE_PATH" | sed 's|/.claude/|/src/claude/|')
    log "  Suggested: $SUGGESTED"

    echo "BLOCKED: Edit targets operational .claude/ directory. Use the src/ tree instead." >&2
    echo "  Target:    $FILE_PATH" >&2
    echo "  Use instead: $SUGGESTED" >&2
    echo "  Only .claude/plans/ and .claude/memory/sessions/ are writable." >&2
    exit 2
  fi

  # --- BLOCK: /tmp/ system directory ---
  if [[ "$FILE_PATH" == /tmp/* || "$FILE_PATH" == */tmp/* ]]; then
    # Allow project-root-relative tmp/ (no leading /)
    if [[ "$FILE_PATH" == "$PROJECT_ROOT/tmp/"* ]]; then
      log "✓ Project-relative tmp/ path allowed: $FILE_PATH"
    else
      log "✗ BLOCKED: Write to /tmp/ system directory"
      echo "BLOCKED: Writing to /tmp/ is forbidden. Use project-relative tmp/{STORY-ID}/ instead." >&2
      echo "  Target:    $FILE_PATH" >&2
      echo "  Use instead: $PROJECT_ROOT/tmp/{STORY-ID}/filename" >&2
      exit 2
    fi
  fi

  # --- BLOCK: src/tests/ (must use tests/{story-id}/) ---
  if [[ "$FILE_PATH" == *"/src/tests/"* ]]; then
    log "✗ BLOCKED: Write to src/tests/ - use tests/{STORY-ID}/ instead"
    echo "BLOCKED: Test files belong in tests/{STORY-ID}/, not src/tests/." >&2
    echo "  Target:    $FILE_PATH" >&2
    echo "  Use instead: $PROJECT_ROOT/tests/{STORY-ID}/your-test-file" >&2
    exit 2
  fi
fi

# ============================================================
# SECTION 2: Bash COMMAND VALIDATION (existing logic, cleaned up)
# ============================================================
# Extract command for Bash tool
COMMAND=$(echo "$TOOL_INPUT" | jq -r '.tool_input.command // empty' 2>/dev/null)
log "Extracted command: '$COMMAND'"

# If not a Bash tool call, auto-approve (Edit/Write path checks already done above)
if [[ "$TOOL_NAME" != "Bash" ]]; then
  log "Non-Bash tool (path checks passed): AUTO-APPROVE"
  log "=========================================="
  exit 0
fi

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
  "bash devforgeai/"
  "echo "
  "cat tests/"
  "cat devforgeai/"
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
  "pytest"
  "wc -l"
  "ls -la"
  "ls -lh"
  "ls -1"
  "ls "
  "cat src/"
  "cat installer/"
  "find installer"
  "find /mnt/c/Projects/DevForgeAI2/installer"
  "find /mnt/c/Projects/DevForgeAI2/src"
  "find /mnt/c/Projects/DevForgeAI2/tests"
  "grep -r"
  "python3 -m py_compile"
  "sort -"
  "cd "
  "python3 -c "
  "python3 << 'EOF'"
  "python << 'EOF'"
  "devforgeai "
  "devforgeai-validate "
  "git rev-parse"
  "git branch"
  "git --version"
  "git rev-list"
  "which "
  "command -v"
  "type "
  "stat "
  "file "
  "basename "
  "pip install"
  "pip3 install"
)

# CRITICAL: Define BLOCKED_PATTERNS before SAFE_PATTERNS loop uses it
BLOCKED_PATTERNS=(
  "rm -rf"
  "sudo"
  "git push"
  "npm publish"
  "curl"
  "wget"
)

log "Checking against ${#SAFE_PATTERNS[@]} safe patterns..."

# RCA-015 REC-02: Quote-aware base command extraction
extract_base_command() {
  local cmd="$1"
  local result=""
  local in_quote=false
  local quote_char=""

  for (( i=0; i<${#cmd}; i++ )); do
    char="${cmd:$i:1}"

    if [ "$in_quote" = false ] && { [ "$char" = "'" ] || [ "$char" = '"' ]; }; then
      in_quote=true
      quote_char="$char"
      result="${result}${char}"
    elif [ "$char" = "$quote_char" ] && [ "$in_quote" = true ]; then
      in_quote=false
      quote_char=""
      result="${result}${char}"
    elif [ "$in_quote" = false ]; then
      case "$char" in
        "|") break ;;
        ">") break ;;
        "2")
          if [ "${cmd:$i:4}" = "2>&1" ] || [ "${cmd:$i:2}" = "2>" ]; then
            break
          else
            result="${result}${char}"
          fi
          ;;
        *) result="${result}${char}" ;;
      esac
    else
      result="${result}${char}"
    fi
  done

  echo "$result"
}

# Enhanced pattern matching with pipe/redirect support
for pattern in "${SAFE_PATTERNS[@]}"; do
  BASE_CMD=$(extract_base_command "$COMMAND")

  if [[ "$BASE_CMD" == "$pattern"* ]]; then
    log "✓ MATCHED safe pattern: '$pattern'"

    if [[ "$COMMAND" != "$BASE_CMD" ]]; then
      log "  Full command: $COMMAND"
      log "  Base extracted: $BASE_CMD"
    fi

    # SAFETY CHECK 1: Verify full command doesn't contain blocked patterns
    for blocked in "${BLOCKED_PATTERNS[@]}"; do
      if [[ "$COMMAND" =~ ${blocked} ]]; then
        log "✗ Base safe BUT full command contains blocked pattern: '$blocked'"
        log "Decision: BLOCK (exit 2)"
        echo '{"decision": "block", "reason": "Command contains dangerous operation: '"$blocked"'"}' >&2
        exit 2
      fi
    done

    # SAFETY CHECK 2: Block redirects to system directories
    if [[ "$COMMAND" =~ \>[[:space:]]*/etc/ ]] || \
       [[ "$COMMAND" =~ \>[[:space:]]*/usr/ ]] || \
       [[ "$COMMAND" =~ \>[[:space:]]*/sys/ ]] || \
       [[ "$COMMAND" =~ \>[[:space:]]*/boot/ ]] || \
       [[ "$COMMAND" =~ \>[[:space:]]*/root/ ]]; then
      log "✗ Redirect to system directory detected"
      log "Decision: BLOCK (exit 2)"
      echo '{"decision": "block", "reason": "Redirect to protected system directory"}' >&2
      exit 2
    fi

    # Safe base + no blocked patterns + no system redirects = auto-approve
    log "Decision: AUTO-APPROVE (exit 0)"
    log "=========================================="
    exit 0
  fi
done

log "No safe pattern matched"

# Near-miss detection for pattern improvement
NEAR_MISSES=()
for pattern in "${SAFE_PATTERNS[@]}"; do
    if [[ "$COMMAND" == *"$pattern"* ]]; then
        NEAR_MISSES+=("$pattern")
    fi
done

if [[ ${#NEAR_MISSES[@]} -gt 0 ]]; then
    log "NEAR-MISS DETECTED"
    log "Command starts with: ${COMMAND:0:20}"
    for nm in "${NEAR_MISSES[@]}"; do
        log "  Near-miss pattern: $nm"
    done
    log "RECOMMENDATION: Command contains safe pattern but doesn't start with it"
fi

# Block anti-patterns
log "Checking against ${#BLOCKED_PATTERNS[@]} blocked patterns..."

for pattern in "${BLOCKED_PATTERNS[@]}"; do
  if [[ "$COMMAND" =~ ${pattern} ]]; then
    log "✗ MATCHED blocked pattern: '$pattern'"
    log "Decision: BLOCK (exit 2)"
    echo '{"decision": "block", "reason": "Dangerous operation: '"$COMMAND"'"}' >&2
    exit 2
  fi
done

log "No blocked pattern matched"

# For all others, ask user for approval
log "Decision: ASK USER (exit 1)"
log "Command requires manual approval: $COMMAND"
log_unknown_command "$COMMAND"
log "=========================================="
exit 1
