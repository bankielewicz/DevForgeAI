#!/bin/bash
# Test: AC#4 - Hook Exits Code 0 Always (Non-Blocking)
# Story: STORY-529
# Verifies: Hook exits 0 for missing files, malformed JSON, no active workflows

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

echo "=== AC#4: Hook Exits Code 0 Always ==="
echo "Target: $HOOK_SCRIPT"
echo ""

SESSION_EVENT='{"event":"SessionStart","source":"resume"}'

# --- Test 1: Hook script exists (prerequisite) ---
run_test "Hook script exists at $HOOK_SCRIPT" \
    "$([ -f "$HOOK_SCRIPT" ] && echo 0 || echo 1)"

# --- Test 2: Exit 0 when no workflows directory exists ---
TMPDIR=$(mktemp -d)
# No devforgeai/workflows/ directory at all
echo "$SESSION_EVENT" | CLAUDE_PROJECT_DIR="$TMPDIR" bash "$HOOK_SCRIPT" >/dev/null 2>&1
EXIT_CODE=$?
run_test "Exit 0 when workflows directory missing" \
    "$([ "$EXIT_CODE" -eq 0 ] && echo 0 || echo 1)"

# --- Test 3: Exit 0 when workflows directory is empty ---
mkdir -p "$TMPDIR/devforgeai/workflows"
echo "$SESSION_EVENT" | CLAUDE_PROJECT_DIR="$TMPDIR" bash "$HOOK_SCRIPT" >/dev/null 2>&1
EXIT_CODE=$?
run_test "Exit 0 when workflows directory is empty (no active workflows)" \
    "$([ "$EXIT_CODE" -eq 0 ] && echo 0 || echo 1)"

# --- Test 4: Exit 0 when phase-state file contains malformed JSON ---
cat > "$TMPDIR/devforgeai/workflows/STORY-666-phase-state.json" <<'BADJSON'
{this is not valid json at all!!!
BADJSON
echo "$SESSION_EVENT" | CLAUDE_PROJECT_DIR="$TMPDIR" bash "$HOOK_SCRIPT" >/dev/null 2>&1
EXIT_CODE=$?
run_test "Exit 0 when phase-state file contains malformed JSON" \
    "$([ "$EXIT_CODE" -eq 0 ] && echo 0 || echo 1)"

# --- Test 5: Exit 0 when phase-state file is empty ---
> "$TMPDIR/devforgeai/workflows/STORY-667-phase-state.json"
echo "$SESSION_EVENT" | CLAUDE_PROJECT_DIR="$TMPDIR" bash "$HOOK_SCRIPT" >/dev/null 2>&1
EXIT_CODE=$?
run_test "Exit 0 when phase-state file is empty" \
    "$([ "$EXIT_CODE" -eq 0 ] && echo 0 || echo 1)"

# --- Test 6: Exit 0 when only QA phase-state files exist ---
rm -f "$TMPDIR/devforgeai/workflows/STORY-666-phase-state.json"
rm -f "$TMPDIR/devforgeai/workflows/STORY-667-phase-state.json"
cat > "$TMPDIR/devforgeai/workflows/STORY-668-qa-phase-state.json" <<'QAJSON'
{
  "story_id": "STORY-668",
  "type": "qa",
  "current_phase": "01"
}
QAJSON
echo "$SESSION_EVENT" | CLAUDE_PROJECT_DIR="$TMPDIR" bash "$HOOK_SCRIPT" >/dev/null 2>&1
EXIT_CODE=$?
run_test "Exit 0 when only QA phase-state files exist" \
    "$([ "$EXIT_CODE" -eq 0 ] && echo 0 || echo 1)"

# --- Test 7: Exit 0 with valid workflow (normal happy path) ---
rm -f "$TMPDIR/devforgeai/workflows/STORY-668-qa-phase-state.json"
cat > "$TMPDIR/devforgeai/workflows/STORY-669-phase-state.json" <<'GOODJSON'
{
  "story_id": "STORY-669",
  "current_phase": "02",
  "phases": {
    "01": {"name": "Pre-Flight", "status": "completed", "completed": true},
    "02": {"name": "Test-First", "status": "in_progress", "completed": false}
  },
  "created": "2026-03-01T10:00:00Z"
}
GOODJSON
echo "$SESSION_EVENT" | CLAUDE_PROJECT_DIR="$TMPDIR" bash "$HOOK_SCRIPT" >/dev/null 2>&1
EXIT_CODE=$?
run_test "Exit 0 with valid active workflow (happy path)" \
    "$([ "$EXIT_CODE" -eq 0 ] && echo 0 || echo 1)"

# --- Test 8: Warnings go to stderr, not stdout ---
STDERR_OUT=$(echo "$SESSION_EVENT" | CLAUDE_PROJECT_DIR="$TMPDIR" bash "$HOOK_SCRIPT" 2>&1 >/dev/null)
STDOUT_OUT=$(echo "$SESSION_EVENT" | CLAUDE_PROJECT_DIR="$TMPDIR" bash "$HOOK_SCRIPT" 2>/dev/null)
# Stdout should be JSON or empty, never contain warning text
run_test "Warnings go to stderr not stdout" \
    "$(echo "$STDOUT_OUT" | grep -qvi "warning\|error\|WARN" && echo 0 || echo 1)"

echo ""
echo "Results: $PASS passed, $FAIL failed"
[ "$FAIL" -eq 0 ] && exit 0 || exit 1
