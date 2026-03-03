#!/bin/bash
# Test: AC#1 - Block Incomplete Phases
# Story: STORY-528
# Verifies: Hook exits code 2 when active workflow has incomplete phases

set -uo pipefail

HOOK_SCRIPT="src/claude/hooks/phase-completion-gate.sh"
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

echo "=== AC#1: Block Incomplete Phases ==="
echo "Target: $HOOK_SCRIPT"
echo ""

# --- Test 1: Hook script exists ---
run_test "Hook script exists at $HOOK_SCRIPT" \
    "$([ -f "$HOOK_SCRIPT" ] && echo 0 || echo 1)"

# --- Test 2: Hook exits code 2 for incomplete phases ---
TMPDIR=$(mktemp -d)
mkdir -p "$TMPDIR/devforgeai/workflows"

# Create phase-state with incomplete phases
cat > "$TMPDIR/devforgeai/workflows/STORY-999-phase-state.json" <<'PHASEJSON'
{
  "story_id": "STORY-999",
  "phases": {
    "01": {"name": "Pre-Flight", "status": "completed", "completed": true},
    "02": {"name": "Test-First", "status": "completed", "completed": true},
    "03": {"name": "Implementation", "status": "in_progress", "completed": false},
    "04": {"name": "Refactoring", "status": "pending", "completed": false}
  }
}
PHASEJSON

STOP_EVENT='{"event":"Stop","reason":"user_request"}'

STDERR_OUTPUT=$(echo "$STOP_EVENT" | CLAUDE_PROJECT_DIR="$TMPDIR" bash "$HOOK_SCRIPT" 2>&1 >/dev/null)
EXIT_CODE=$?

run_test "Hook exits code 2 when phases incomplete" \
    "$([ "$EXIT_CODE" -eq 2 ] && echo 0 || echo 1)"

# --- Test 3: Stderr reports incomplete phases ---
run_test "Stderr mentions incomplete phase 03" \
    "$(echo "$STDERR_OUTPUT" | grep -q "03\|Implementation\|in_progress" && echo 0 || echo 1)"

run_test "Stderr mentions incomplete phase 04" \
    "$(echo "$STDERR_OUTPUT" | grep -q "04\|Refactoring\|pending" && echo 0 || echo 1)"

# --- Test 4: Stderr contains story ID ---
run_test "Stderr contains story ID STORY-999" \
    "$(echo "$STDERR_OUTPUT" | grep -q "STORY-999" && echo 0 || echo 1)"

echo ""
echo "Results: $PASS passed, $FAIL failed"
[ "$FAIL" -eq 0 ] && exit 0 || exit 1
