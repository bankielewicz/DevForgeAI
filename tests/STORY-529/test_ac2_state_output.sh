#!/bin/bash
# Test: AC#2 - Hook Discovers Active Phase State and Outputs Summary
# Story: STORY-529
# Verifies: Stdout is valid JSON with hookSpecificOutput.additionalContext containing workflow summary

set -uo pipefail

HOOK_SCRIPT="src/claude/hooks/inject-phase-context.sh"
PASS=0
FAIL=0
TMPDIR=""

cleanup() {
    [ -n "$TMPDIR" ] && rm -rf "$TMPDIR"
}
trap cleanup EXIT

run_test() {
    local description="$1"
    local result="$2"
    if [ "$result" -eq 0 ]; then
        echo "PASS: $description"
        ((PASS++))
    else
        echo "FAIL: $description"
        ((FAIL++))
    fi
}

echo "=== AC#2: Hook Discovers Active Phase State and Outputs Summary ==="
echo "Target: $HOOK_SCRIPT"
echo ""

# --- Setup: Create temp project with active workflow ---
TMPDIR=$(mktemp -d)
mkdir -p "$TMPDIR/devforgeai/workflows"

cat > "$TMPDIR/devforgeai/workflows/STORY-800-phase-state.json" <<'PHASEJSON'
{
  "story_id": "STORY-800",
  "current_phase": "04",
  "phases": {
    "01": {"name": "Pre-Flight", "status": "completed", "completed": true},
    "02": {"name": "Test-First", "status": "completed", "completed": true},
    "03": {"name": "Implementation", "status": "completed", "completed": true},
    "04": {"name": "Refactoring", "status": "in_progress", "completed": false},
    "05": {"name": "Integration", "status": "pending", "completed": false}
  },
  "subagents_invoked": ["git-validator", "test-automator", "backend-architect"],
  "created": "2026-03-01T12:00:00Z"
}
PHASEJSON

SESSION_EVENT='{"event":"SessionStart","source":"compact"}'
STDOUT_OUTPUT=$(echo "$SESSION_EVENT" | CLAUDE_PROJECT_DIR="$TMPDIR" bash "$HOOK_SCRIPT" 2>/dev/null)

# --- Test 1: Stdout is valid JSON ---
run_test "Stdout is valid JSON" \
    "$(echo "$STDOUT_OUTPUT" | python3 -c 'import json,sys; json.load(sys.stdin)' 2>/dev/null && echo 0 || echo 1)"

# --- Test 2: JSON has hookSpecificOutput key ---
HAS_HSO=$(echo "$STDOUT_OUTPUT" | python3 -c "
import json, sys
data = json.load(sys.stdin)
print('yes' if 'hookSpecificOutput' in data else 'no')
" 2>/dev/null || echo "no")
run_test "JSON contains hookSpecificOutput key" \
    "$([ "$HAS_HSO" = "yes" ] && echo 0 || echo 1)"

# --- Test 3: hookSpecificOutput has hookEventName = SessionStart ---
EVENT_NAME=$(echo "$STDOUT_OUTPUT" | python3 -c "
import json, sys
data = json.load(sys.stdin)
print(data.get('hookSpecificOutput', {}).get('hookEventName', ''))
" 2>/dev/null || echo "")
run_test "hookEventName is SessionStart" \
    "$([ "$EVENT_NAME" = "SessionStart" ] && echo 0 || echo 1)"

# --- Test 4: hookSpecificOutput has additionalContext ---
HAS_CTX=$(echo "$STDOUT_OUTPUT" | python3 -c "
import json, sys
data = json.load(sys.stdin)
ctx = data.get('hookSpecificOutput', {}).get('additionalContext', '')
print('yes' if ctx else 'no')
" 2>/dev/null || echo "no")
run_test "hookSpecificOutput contains non-empty additionalContext" \
    "$([ "$HAS_CTX" = "yes" ] && echo 0 || echo 1)"

# --- Test 5: additionalContext contains story ID ---
CONTEXT=$(echo "$STDOUT_OUTPUT" | python3 -c "
import json, sys
data = json.load(sys.stdin)
print(data.get('hookSpecificOutput', {}).get('additionalContext', ''))
" 2>/dev/null || echo "")
run_test "additionalContext contains story ID STORY-800" \
    "$(echo "$CONTEXT" | grep -q "STORY-800" && echo 0 || echo 1)"

# --- Test 6: additionalContext contains current phase ---
run_test "additionalContext contains current phase number or name" \
    "$(echo "$CONTEXT" | grep -qi "04\|refactor" && echo 0 || echo 1)"

# --- Test 7: additionalContext contains steps_completed ---
run_test "additionalContext contains steps_completed info" \
    "$(echo "$CONTEXT" | grep -qi "steps.completed\|steps completed\|completed.*3" && echo 0 || echo 1)"

# --- Test 8: additionalContext contains steps remaining ---
run_test "additionalContext contains steps remaining info" \
    "$(echo "$CONTEXT" | grep -qi "steps.remain\|remaining\|remain" && echo 0 || echo 1)"

# --- Test 9: additionalContext contains subagents_invoked ---
run_test "additionalContext contains subagents invoked" \
    "$(echo "$CONTEXT" | grep -qi "subagent.*invoked\|invoked.*subagent\|git-validator\|test-automator" && echo 0 || echo 1)"

# --- Test 10: additionalContext contains subagents required ---
run_test "additionalContext contains subagents required info" \
    "$(echo "$CONTEXT" | grep -qi "required\|needed\|remaining.*subagent" && echo 0 || echo 1)"

# --- Test 11: QA phase-state files are excluded ---
cat > "$TMPDIR/devforgeai/workflows/STORY-800-qa-phase-state.json" <<'QAJSON'
{
  "story_id": "STORY-800",
  "type": "qa",
  "current_phase": "01"
}
QAJSON

STDOUT_WITH_QA=$(echo "$SESSION_EVENT" | CLAUDE_PROJECT_DIR="$TMPDIR" bash "$HOOK_SCRIPT" 2>/dev/null)
CONTEXT_WITH_QA=$(echo "$STDOUT_WITH_QA" | python3 -c "
import json, sys
data = json.load(sys.stdin)
print(data.get('hookSpecificOutput', {}).get('additionalContext', ''))
" 2>/dev/null || echo "")
# QA file should not affect output - story ID should still be STORY-800 from dev workflow
run_test "QA phase-state files are excluded from discovery" \
    "$(echo "$CONTEXT_WITH_QA" | grep -qv 'type.*qa' && echo 0 || echo 1)"

# --- Test 12: Most recent workflow selected when multiple exist ---
cat > "$TMPDIR/devforgeai/workflows/STORY-700-phase-state.json" <<'OLDJSON'
{
  "story_id": "STORY-700",
  "current_phase": "02",
  "phases": {
    "01": {"name": "Pre-Flight", "status": "completed", "completed": true},
    "02": {"name": "Test-First", "status": "in_progress", "completed": false}
  },
  "created": "2026-02-28T08:00:00Z"
}
OLDJSON

STDOUT_MULTI=$(echo "$SESSION_EVENT" | CLAUDE_PROJECT_DIR="$TMPDIR" bash "$HOOK_SCRIPT" 2>/dev/null)
CONTEXT_MULTI=$(echo "$STDOUT_MULTI" | python3 -c "
import json, sys
data = json.load(sys.stdin)
print(data.get('hookSpecificOutput', {}).get('additionalContext', ''))
" 2>/dev/null || echo "")
run_test "Most recent workflow (STORY-800) selected over older (STORY-700)" \
    "$(echo "$CONTEXT_MULTI" | grep -q "STORY-800" && echo 0 || echo 1)"

echo ""
echo "Results: $PASS passed, $FAIL failed"
[ "$FAIL" -eq 0 ] && exit 0 || exit 1
